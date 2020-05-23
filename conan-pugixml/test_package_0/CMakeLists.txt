#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project("test_package" VERSION 1.0 LANGUAGES CXX)

#=======================================
#                 CONAN                 
#=======================================

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#=======================================
#               EXECUTABLE              
#======================================= 

add_executable(
	${PROJECT_NAME}
	../test_package/test_package.cpp
	)

file(COPY "../test_package/example.xml" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

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

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})