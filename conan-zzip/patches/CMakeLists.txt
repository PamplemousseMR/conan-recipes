cmake_minimum_required(VERSION 2.8)
project(cmakeWrapper)

set(ZZIP_CONAN_INFO_DIR CACHE PATH "directory which contain the conanbuildinfo.cmake")
include(${ZZIP_CONAN_INFO_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include("WrappedCMakeLists.txt")