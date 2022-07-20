#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string *) userp)->append((char *) contents, size * nmemb);
    return size * nmemb;
}

int main(int argc, char* argv[])
{
    if (argc != 3 || std::string(argv[1]) == "--help") {
        std::cerr << "Usage: ./compare_face <path_to_the_"
                                    "first_photo> <path_to_the_second_photo>";
        return 0;
    }

    CURL *curl;
    CURLcode res;

    struct curl_httppost *formpost = nullptr;
    struct curl_httppost *lastptr = nullptr;
    struct curl_slist *list = nullptr;
    std::string body;

    curl_formadd(&formpost,
                 &lastptr,
                 CURLFORM_COPYNAME, "source_image",
                 CURLFORM_FILE, argv[1],
                 CURLFORM_END);

    curl_formadd(&formpost,
                 &lastptr,
                 CURLFORM_COPYNAME, "target_image",
                 CURLFORM_FILE, argv[2],
                 CURLFORM_END);

    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000/api/v1/verification/verify");

        list = curl_slist_append(list, "x-api-key: 00000000-0000-0000-0000-000000000004");

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, formpost);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &body);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        curl_easy_cleanup(curl);
        curl_formfree(formpost);
        curl_slist_free_all(list);
    }

    auto j = json::parse(body);
    std::cout << j.at("result")[0].at("face_matches")[0].at("similarity").dump();
    return 0;
}
