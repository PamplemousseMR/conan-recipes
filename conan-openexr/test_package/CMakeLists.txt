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
	
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/comp_short_decode_piz.exr DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

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

find_package(OpenEXR REQUIRED CONFIG)

target_link_libraries(${PROJECT_NAME} OpenEXR::IlmImfConfig OpenEXR::IlmImf OpenEXR::IlmImfUtil)

find_package(IlmBase REQUIRED CONFIG)

target_link_libraries(${PROJECT_NAME} IlmBase::IlmBaseConfig IlmBase::Half IlmBase::Iex IlmBase::IexMath IlmBase::Imath IlmBase::IlmThread)