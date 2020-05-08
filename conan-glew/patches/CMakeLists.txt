#=======================================
#                PROJECT                
#=======================================

project(glew)
cmake_minimum_required(VERSION 3.0)

#=======================================
#                 INIT                 
#======================================= 

#---------------------------------------
#               VARIABLES               
#---------------------------------------

set(GLEW_PROJECT_NAME "glew")
set(INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE PATH "Installation directory for executables")
set(INSTALL_LIB_DIR "${CMAKE_INSTALL_PREFIX}/lib" CACHE PATH "Installation directory for libraries")
set(INSTALL_INC_DIR "${CMAKE_INSTALL_PREFIX}/include" CACHE PATH "Installation directory for headers")

#---------------------------------------
#                 FILES                 
#---------------------------------------

set(GLEW_SRC_FILES src/glew)
file(GLOB GLEW_HEADER_FILES include/*)

#--------------------------------------- 
#                COMPILER                
#---------------------------------------

option(GLEW_MX "Build Glew with Multiple Rendering Contexts." ON)
if(GLEW_MX)
    add_definitions(-DGLEW_MX)
endif()

if(WIN32)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    list(APPEND GLEW_SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/build/glew.rc)
endif()

#=======================================
#                CREATE                
#=======================================

#---------------------------------------
#                  LIB                  
#---------------------------------------

if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    if(BUILD_SHARED_LIBS)
        set(GLEW_LIB_NAME "glew32")
    else()
        set(GLEW_LIB_NAME "glew32s")
    endif()
else(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    if(BUILD_SHARED_LIBS)
        set(GLEW_LIB_NAME "libGLEW")
    else()
        set(GLEW_LIB_NAME "glew_static")
    endif()
endif(${CMAKE_SYSTEM_NAME} MATCHES "Windows")

add_library(${GLEW_PROJECT_NAME} ${GLEW_SRC_FILES} ${GLEW_HEADER_FILES})

if(BUILD_SHARED_LIBS)
    add_definitions(-DGLEW_BUILD)
else()
    add_definitions(-DGLEW_STATIC)
endif()

set_target_properties(${GLEW_PROJECT_NAME} PROPERTIES OUTPUT_NAME ${GLEW_LIB_NAME})
target_include_directories(${GLEW_PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

#---------------------------------------
#                OPENGL                
#---------------------------------------

find_package(OpenGL REQUIRED)

target_include_directories(${GLEW_PROJECT_NAME} PRIVATE ${OPENGL_INCLUDE_DIR})
target_link_libraries(${GLEW_PROJECT_NAME} OpenGL::GL)

#---------------------------------------
#                INSTALL                
#---------------------------------------

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/GL" DESTINATION "${INSTALL_INC_DIR}")

install(TARGETS ${GLEW_PROJECT_NAME}
        RUNTIME DESTINATION "${INSTALL_BIN_DIR}"
        ARCHIVE DESTINATION "${INSTALL_LIB_DIR}"
        LIBRARY DESTINATION "${INSTALL_LIB_DIR}")