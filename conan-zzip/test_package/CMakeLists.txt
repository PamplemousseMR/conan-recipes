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

find_package(ZZip REQUIRED)

if("${ZZip_VERSION}" VERSION_LESS_EQUAL "0.13.72")
	target_include_directories(${PROJECT_NAME} PRIVATE ${ZZip_INCLUDE_DIRS})
	target_link_libraries(${PROJECT_NAME} PRIVATE ${ZZip_LIBRARIES})
else()
	message(FATAL_ERROR "Unhandle version " ${ZZip_VERSION})
endif()