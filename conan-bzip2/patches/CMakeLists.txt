#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 2.8)
project(bzip2 C)

#=======================================
#                 INIT                 
#======================================= 

#---------------------------------------
#               VARIABLES               
#---------------------------------------

option(BZIP2_BUILD_EXE OFF)

#---------------------------------------
#                 FILES                 
#---------------------------------------

set(BZIP2_PROJECT_NAME "bz2")
set(BZIP2_SRC_FILES "blocksort.c" "bzlib.c" "compress.c" "crctable.c" "decompress.c" "huffman.c" "randtable.c")

#--------------------------------------- 
#                COMPILER                
#---------------------------------------

if(MSVC OR MSVC90 OR MSVC10)
  set(MSVC ON)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif(MSVC OR MSVC90 OR MSVC10)

#=======================================
#                CREATE                
#=======================================

#---------------------------------------
#                  LIB                  
#---------------------------------------

add_library(${BZIP2_PROJECT_NAME} ${BZIP2_SRC_FILES})

if(BZIP2_BUILD_EXE)
    add_executable(${CMAKE_PROJECT_NAME} "bzip2.c")
    target_link_libraries(${CMAKE_PROJECT_NAME} ${BZIP2_PROJECT_NAME})
    target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE ${BZIP2_SRC_FILES})
endif(BZIP2_BUILD_EXE)

#---------------------------------------
#                INSTALL                
#---------------------------------------

install(FILES "bzlib.h" DESTINATION "include")

install(TARGETS ${BZIP2_PROJECT_NAME}
        RUNTIME DESTINATION "bin"
        LIBRARY DESTINATION "lib"
        ARCHIVE DESTINATION "lib")

if(BZIP2_BUILD_EXE)
    install(TARGETS ${CMAKE_PROJECT_NAME}
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
            ARCHIVE DESTINATION lib)
endif(BZIP2_BUILD_EXE)