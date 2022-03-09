cmake_minimum_required(VERSION 3.18)
project(Skytran_6DOF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXE_LINKER_FLAGS "-static")

add_executable(Skytran_6DOF src/main.cpp)

if (MINGW)
    target_link_libraries(Skytran_6DOF ws2_32)
endif ()
