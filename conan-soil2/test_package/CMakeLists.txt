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

find_package(SOIL2 REQUIRED CONFIG)

if("${SOIL2_VERSION}" VERSION_LESS_EQUAL "1.20")
	target_link_libraries(${PROJECT_NAME} PRIVATE SOIL2::SOIL2)
else()
	message(FATAL_ERROR "Unhandle version " ${SOIL2_VERSION})
endif()
