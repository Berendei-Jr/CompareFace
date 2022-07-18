cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 17)
include("cmake/HunterGate.cmake")

HunterGate(
        URL "https://github.com/cpp-pm/hunter/archive/v0.23.297.tar.gz"
        SHA1 "3319fe6a3b08090df7df98dee75134d68e2ef5a3"
)

project(TestProject)

hunter_add_package(CURL)
find_package(CURL CONFIG REQUIRED)
find_package(Threads)

add_library(${PROJECT_NAME} STATIC
        ${CMAKE_CURRENT_SOURCE_DIR}/sources/source.cpp
        )

target_include_directories(${PROJECT_NAME} PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:include>"
        "{CURL_ROOT}/include"
        )

add_executable(test main.cpp)

target_link_libraries(test ${PROJECT_NAME}
        CURL::libcurl
        Threads::Threads
        )
