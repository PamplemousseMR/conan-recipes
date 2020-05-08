#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 2.8)
project(SOIL2)

#=======================================
#                 INIT                 
#=======================================

#---------------------------------------
#               VARIABLES               
#---------------------------------------

set(SOIL_PROJECT_NAME "SOIL2")

#---------------------------------------
#                 FILES                 
#---------------------------------------

file(GLOB SOIL_SRC_FILES src/SOIL2/*.c)
file(GLOB SOIL_HEADER_FILES src/SOIL2/*.h)

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

add_library(${SOIL_PROJECT_NAME} ${SOIL_SRC_FILES} ${SOIL_HEADER_FILES})

#---------------------------------------
#                OPENGL                
#---------------------------------------

find_package(OpenGL REQUIRED)

target_link_libraries(${SOIL_PROJECT_NAME} OpenGL::GL)

#---------------------------------------
#                INSTALL                
#---------------------------------------

install(FILES ${SOIL_HEADER_FILES} DESTINATION "include/SOIL2")

install(TARGETS ${SOIL_PROJECT_NAME}
        RUNTIME DESTINATION "bin"
        LIBRARY DESTINATION "lib"
        ARCHIVE DESTINATION "lib")
