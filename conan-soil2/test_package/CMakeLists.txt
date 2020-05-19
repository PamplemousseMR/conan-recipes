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
#                 SOIL2                 
#---------------------------------------

find_package(SOIL2 REQUIRED CONFIG)

target_link_libraries(${TEST_PACKAGE_PROJECT_NAME} SOIL2::SOIL2)