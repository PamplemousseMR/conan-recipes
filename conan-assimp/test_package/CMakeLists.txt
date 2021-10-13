#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project("test_package" VERSION 1.0 LANGUAGES CXX)

#=======================================
#               EXECUTABLE              
#======================================= 

add_executable(
	${PROJECT_NAME}
	test_package.cpp
	)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/box.obj DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

#=======================================
#                SETTINGS               
#=======================================

set_target_properties(
	${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    )

#=======================================
#                PACKAGE                
#=======================================

find_package(assimp REQUIRED)

if("${assimp_VERSION}" VERSION_LESS_EQUAL "5.0.1")
	target_link_libraries(${PROJECT_NAME} PRIVATE assimp::assimp)
else()
	message(FATAL_ERROR "Unhandle version " ${assimp_VERSION})
endif()