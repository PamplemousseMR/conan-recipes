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
	
file(COPY ../test_package/comp_short_decode_piz.exr DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

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

find_package(OpenEXR REQUIRED)

if("${OpenEXR_VERSION}" VERSION_LESS_EQUAL "2.5.3")
	target_link_libraries(${PROJECT_NAME} OpenEXR::IlmImfConfig OpenEXR::IlmImf OpenEXR::IlmImfUtil)
elseif("${OpenEXR_VERSION}" VERSION_LESS_EQUAL "3.0.5")
	target_link_libraries(${PROJECT_NAME} OpenEXR::OpenEXRConfig OpenEXR::IexConfig OpenEXR::IlmThreadConfig OpenEXR::Iex OpenEXR::IlmThread OpenEXR::OpenEXR OpenEXR::OpenEXRUtil)
elseif("${OpenEXR_VERSION}" VERSION_LESS_EQUAL "3.1.1")
	target_link_libraries(${PROJECT_NAME} OpenEXR::OpenEXRConfig OpenEXR::IexConfig OpenEXR::IlmThreadConfig OpenEXR::Iex OpenEXR::IlmThread OpenEXR::OpenEXRCore OpenEXR::OpenEXR OpenEXR::OpenEXRUtil)
else()
	message(FATAL_ERROR "Unhandle version " ${OpenEXR_VERSION})
endif()