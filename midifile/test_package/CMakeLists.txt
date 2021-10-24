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

find_package(midifile REQUIRED)


if("${midifile_VERSION}" VERSION_LESS_EQUAL "0.2")
	target_link_libraries(${PROJECT_NAME} midifile::midifile)
else()
	message(FATAL_ERROR "Unhandle version " ${midifile_VERSION})
endif()