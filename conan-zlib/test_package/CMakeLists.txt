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
set(TEST_PACKAGE_SRC_FILES "test_package.cpp")

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
#                 ZLIB                 
#---------------------------------------

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_BINARY_DIR})
find_package(ZLIB REQUIRED)

target_include_directories(${TEST_PACKAGE_PROJECT_NAME} PRIVATE ${ZLIB_INCLUDE_DIRS})
target_link_libraries(${TEST_PACKAGE_PROJECT_NAME} ZLIB::ZLIB)