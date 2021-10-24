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
	addressbook.proto
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

find_package(protobuf REQUIRED CONFIG)

find_program(PROTOC_PROGRAM protoc)
if(NOT PROTOC_PROGRAM)
    message(WARNING "Protoc program was not found")
endif()

if("${protobuf_VERSION}" VERSION_LESS_EQUAL "3.18.0.2")
    if(TARGET protobuf::libprotobuf-lite)
        target_link_libraries(${PROJECT_NAME} protobuf::libprotobuf-lite)
    endif()

    target_link_libraries(${PROJECT_NAME} protobuf::libprotobuf)

    target_link_libraries(${PROJECT_NAME} protobuf::libprotoc)
else()
    message(FATAL_ERROR "Unhandle version " ${protobuf_VERSION})
endif()

target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_BINARY_DIR}")
protobuf_generate(LANGUAGE cpp TARGET ${PROJECT_NAME} PROTOS addressbook.proto)