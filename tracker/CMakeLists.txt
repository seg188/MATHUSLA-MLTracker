cmake_minimum_required(VERSION 3.10)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# set the project name
project(MLTracker)


find_package(ROOT REQUIRED COMPONENTS MathCore Minuit)
find_package(dlib REQUIRED)
find_package(BLAS REQUIRED)

# Defines useful ROOT functions and ROOT macros (e.g. ROOT_GENERATE_DICTIONARY).
include(${ROOT_USE_FILE})

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(tracker-lib SHARED
    src/RunManager.cc
    src/TrackFinder.cc
    src/Digitizer.cc
    src/VertexFinder.cc
    src/Physics.cc
	src/LinearAlgebra.cc
)


target_link_libraries(tracker-lib PUBLIC
    ${ROOT_LIBRARIES}
    ${DLIB_LIBRARIES}
    ${BLAS_LIBRARIES})


# add the executable
add_executable(tracker src/tracking.cc)


# Creates a shared library with a generated dictionary.

target_link_libraries(tracker PUBLIC tracker-lib)



