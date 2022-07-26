#include <iostream>
#include <string>
#include <vector>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string *) userp)->append((char *) contents, size * nmemb);
    return size * nmemb;
}

int main(int argc, char* argv[])
{
    if (argc != 2 || std::string(argv[1]) == "--help") {
        std::cerr << "Usage: ./detect_face <path_to_the_"
                     "photo>";
        return 0;
    }

    CURL *curl;
    CURLcode res;

    struct curl_httppost *formpost = nullptr;
    struct curl_httppost *lastptr = nullptr;
    struct curl_slist *list = nullptr;
    std::string response;

    curl_formadd(&formpost,
                 &lastptr,
                 CURLFORM_COPYNAME, "file",
                 CURLFORM_FILE, argv[1],
                 CURLFORM_END);

    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000/api/v1/detection/detect");

        list = curl_slist_append(list, "x-api-key: 00000000-0000-0000-0000-000000000003");

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, formpost);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        res = curl_easy_perform(curl);

        curl_easy_cleanup(curl);
        curl_formfree(formpost);
        curl_slist_free_all(list);

        if(res != CURLE_OK) {
            fprintf(stderr, "Sending request failed: %s",
                    curl_easy_strerror(res));
            exit(EXIT_FAILURE);
        }
    }

    auto j = json::parse(response);

    if (j.contains("message")) {
        std::cout << "Error occurred: " << j.at("message").dump()
                  << "\nCode: " << j.at("code").dump() << std::endl;
        return 1;
    }

    std::cout << j.at("result").size();
}
