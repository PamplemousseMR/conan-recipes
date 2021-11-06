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
	../test_package/test_package.cpp
	)
	
file(COPY ../test_package/example.xml DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

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

find_package(pugixml REQUIRED) 

if("${pugixml_VERSION}" VERSION_LESS_EQUAL "1.10")
	target_link_libraries(${PROJECT_NAME} PRIVATE pugixml)
elseif("${pugixml_VERSION}" VERSION_LESS_EQUAL "1.11.4")
	target_link_libraries(${PROJECT_NAME} PRIVATE pugixml::pugixml)
else()
	message(FATAL_ERROR "Unhandle version " ${pugixml_VERSION})
endif()
