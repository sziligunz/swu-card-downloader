cmake_minimum_required(VERSION 3.20)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(hailmary)

# CPR
include(FetchContent)
FetchContent_Declare(
    cpr
    GIT_REPOSITORY https://github.com/libcpr/cpr.git
    GIT_TAG master
)
FetchContent_MakeAvailable(cpr)

file(GLOB IMPLEMENTATIONS src/include/*.cpp)

add_executable(hailmary src/steal.cpp ${IMPLEMENTATIONS})

target_include_directories(hailmary PRIVATE src/include)
target_link_libraries(hailmary PRIVATE cpr::cpr)

set_target_properties(hailmary PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)