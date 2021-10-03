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

find_package(glew REQUIRED CONFIG)

if("${glew_VERSION}" VERSION_LESS_EQUAL "2.2.0")
	if(TARGET GLEW::glew)
	target_link_libraries(${PROJECT_NAME} GLEW::glew)
	else()
		target_link_libraries(${PROJECT_NAME} GLEW::glew_s)
	endif()
else()
	message(FATAL_ERROR "Unhandle version " ${glew_VERSION})
endif()