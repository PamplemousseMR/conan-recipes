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

find_package(Imath REQUIRED CONFIG)

if("${Imath_VERSION}" VERSION_LESS_EQUAL "3.1.3")
	target_link_libraries(${PROJECT_NAME} Imath::ImathConfig Imath::Imath)
else()
	message(FATAL_ERROR "Unhandle version " ${Imath_VERSION})
endif()