#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 2.8)
project(test_package CXX)

#=======================================
#                 INIT                 
#======================================= 

#---------------------------------------
#                 FILES                 
#---------------------------------------

set(TEST_PACKAGE_PROJECT_NAME "test_package")
set(TEST_PACKAGE_SRC_FILES "../test_package/test_package.cpp")

#---------------------------------------
#                 CONAN                 
#---------------------------------------

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#--------------------------------------- 
#                COMPILER                
#---------------------------------------

set(CMAKE_CXX_STANDARD 14)

#=======================================
#                CREATE                
#=======================================

#---------------------------------------
#                  EXE                  
#---------------------------------------

add_executable(${TEST_PACKAGE_PROJECT_NAME} ${TEST_PACKAGE_SRC_FILES})

#---------------------------------------
#                LIBPNG                
#---------------------------------------

target_link_libraries(${TEST_PACKAGE_PROJECT_NAME} ${CONAN_LIBS})
