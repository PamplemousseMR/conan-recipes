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
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    if((CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL "3.8.0") AND (CMAKE_CXX_COMPILER_VERSION VERSION_LESS_EQUAL "3.9.1"))
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
    endif()
endif()

#=======================================
#                CREATE                
#=======================================

#---------------------------------------
#                  EXE                  
#---------------------------------------

add_executable(${TEST_PACKAGE_PROJECT_NAME} ${TEST_PACKAGE_SRC_FILES})

#---------------------------------------
#                MIDIFILE               
#---------------------------------------

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_BINARY_DIR})
find_package(midifile REQUIRED)

target_include_directories(${TEST_PACKAGE_PROJECT_NAME} PRIVATE ${midifile_INCLUDE_DIRS})
target_link_libraries(${TEST_PACKAGE_PROJECT_NAME} midifile::midifile)