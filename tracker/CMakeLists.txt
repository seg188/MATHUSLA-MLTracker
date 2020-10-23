cmake_minimum_required(VERSION 3.10)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# set the project name
project(MLTracker)


find_package(ROOT 6.22 CONFIG REQUIRED)

# Defines useful ROOT functions and ROOT macros (e.g. ROOT_GENERATE_DICTIONARY).
include(${ROOT_USE_FILE})

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)


# add the executable
add_executable(MLTracker tracking.cc)

# Creates a shared library with a generated dictionary.
target_link_libraries(MLTracker ${ROOT_LIBRARIES})





