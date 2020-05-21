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

pkg_check_modules(pugixml REQUIRED pugixml)

target_link_libraries(${PROJECT_NAME} PkgConfig::pugixml)
