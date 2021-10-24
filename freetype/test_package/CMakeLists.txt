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

find_package(BZip2 CONFIG)
find_package(PNG)
find_package(Freetype REQUIRED CONFIG)

if("${Freetype_VERSION}" VERSION_LESS_EQUAL "2.11.0")
	target_link_libraries(${PROJECT_NAME} freetype)
	if(BZip2_FOUND)
		target_link_libraries(${PROJECT_NAME} BZip2::bz2)
	endif()
	if(PNG_FOUND)
		target_link_libraries(${PROJECT_NAME} PNG::PNG)
	endif()
else()
	message(FATAL_ERROR "Unhandle version " ${Freetype_VERSION})
endif()