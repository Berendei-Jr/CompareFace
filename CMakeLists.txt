cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 17)
include("cmake/HunterGate.cmake")

HunterGate(
        URL "https://github.com/cpp-pm/hunter/archive/v0.23.297.tar.gz"
        SHA1 "3319fe6a3b08090df7df98dee75134d68e2ef5a3"
)

project(CompareFace)

hunter_add_package(CURL)
hunter_add_package(nlohmann_json)

find_package(CURL CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_library(${PROJECT_NAME} STATIC
        ${CMAKE_CURRENT_SOURCE_DIR}/sources/source.cpp
)

target_include_directories(${PROJECT_NAME} PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:include>"
)

add_executable(compare_face compareFace.cpp)
add_executable(detect_face detectFaces.cpp)

target_link_libraries(compare_face ${PROJECT_NAME}
        CURL::libcurl
        nlohmann_json::nlohmann_json
)

target_link_libraries(detect_face ${PROJECT_NAME}
        CURL::libcurl
        nlohmann_json::nlohmann_json
)
