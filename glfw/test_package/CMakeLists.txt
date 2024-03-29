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

find_package(glfw3 REQUIRED CONFIG)

if("${glfw3_VERSION}" VERSION_LESS_EQUAL "3.3.4")
	target_link_libraries(${PROJECT_NAME} glfw)
else()
	message(FATAL_ERROR "Unhandle version " ${glfw3_VERSION})
endif()