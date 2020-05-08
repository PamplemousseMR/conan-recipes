cmake_minimum_required(VERSION 2.8)
project(cmakeWrapper)

set(FT_CONAN_INFO_DIR CACHE PATH "directory which contain the conanbuildinfo.cmake")
include(${FT_CONAN_INFO_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include("WrappedCMakeLists.txt")