cmake_minimum_required(VERSION 3.18)
project(Skytran_6DOF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXE_LINKER_FLAGS "-static")

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(ClangFormat)

include_directories(${CMAKE_SOURCE_DIR}/include)
link_directories(${CMAKE_SOURCE_DIR}/lib)

add_executable(Skytran_6DOF src/main.cpp)
target_link_libraries(Skytran_6DOF nfd)

if (MINGW)
    target_link_libraries(Skytran_6DOF ws2_32)
endif ()

target_clangformat_setup(${PROJECT_NAME})

add_custom_target(clangtidy
    COMMAND
      clang-tidy
      -p ./build
      --fix-notes
      --fix-errors
      ./src/*
    WORKING_DIRECTORY
      ${CMAKE_SOURCE_DIR}
    COMMENT
      "Running Clang Tidy..."
  )
