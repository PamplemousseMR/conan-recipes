#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project(IrrXML VERSION 1.2 LANGUAGES CXX)

#=======================================
#                SETTINGS               
#=======================================

set(IRRXML_TARGET_NAME ${PROJECT_NAME})

# Set the Cxx standard.
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CXX_STANDARD 11)

# Export all symbols on Windows.
if(MSVC OR MSVC90 OR MSVC10)
  set(MSVC ON)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Set standard installation directories.
set(IRRXML_RUNTIME_DESTINATION "bin")
set(IRRXML_LIBRARY_DESTINATION "lib")
set(IRRXML_ARCHIVE_DESTINATION "lib")
set(IRRXML_INCLUDES_DESTINATION "include")

# Set CMake targets name, namespace and install directory.
set(IRRXML_CMAKE_TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(IRRXML_CMAKE_TARGETS_NAMESPACE "${PROJECT_NAME}::")

# CMake config files name.
set(IRRXML_CMAKE_VERSION_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(IRRXML_CMAKE_PROJECT_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake")

# CMake config files destination.
if(WIN32 AND NOT CYGWIN)
	set(IRRXML_CMAKE_CONFIG_DESTINATION "CMake")
else()
	set(IRRXML_CMAKE_CONFIG_DESTINATION "${IRRXML_LIBRARY_DESTINATION}/cmake/${PROJECT_NAME}")
endif()

#=======================================
#                LIBRARY                
#=======================================

# Store header files.
set(
	IRRXML_HEADER_FILES
	src/CXMLReaderImpl.h
	src/fast_atof.h
	src/heapsort.h
	src/irrArray.h
	src/irrString.h
	src/irrTypes.h
	src/irrXML.h
	)

# Create the library (headers are here since some IDE need them here).
add_library(
	${IRRXML_TARGET_NAME} 
	src/irrXML.cpp
	${IRRXML_HEADER_FILES}
	)

# Add include directory (includes may not be at the same place between build and install).
target_include_directories(
    ${IRRXML_TARGET_NAME}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    $<INSTALL_INTERFACE:${IRRXML_INCLUDES_DESTINATION}>
)

if(MSVC)
  target_compile_definitions(${IRRXML_TARGET_NAME} PRIVATE _SCL_SECURE_NO_WARNINGS)
  target_compile_definitions(${IRRXML_TARGET_NAME} PRIVATE _CRT_SECURE_NO_WARNINGS)
endif(MSVC)

#=======================================
#                CONFIG                 
#=======================================

# Include write_basic_package_version_file and configure_package_config_file.
include(CMakePackageConfigHelpers)

# Generate basic config version files (IrrXmlConfigVersion.cmake).
write_basic_package_version_file(
    ${IRRXML_CMAKE_VERSION_CONFIG_FILE} 
    VERSION ${PROJECT_VERSION} 
    COMPATIBILITY SameMajorVersion
)

# Configure the config.cmake.in
configure_package_config_file(
	"${CMAKE_SOURCE_DIR}/IrrXMLConfig.cmake.in" ${IRRXML_CMAKE_PROJECT_CONFIG_FILE} 
	INSTALL_DESTINATION  ${IRRXML_CMAKE_CONFIG_DESTINATION}
	PATH_VARS IRRXML_INCLUDES_DESTINATION IRRXML_CMAKE_CONFIG_DESTINATION IRRXML_TARGET_NAME IRRXML_LIBRARY_DESTINATION
	)

# Install cmake config files (IRRXMLConfigVersion.cmake and IRRXMLConfig.cmake).
install(
    FILES ${IRRXML_CMAKE_VERSION_CONFIG_FILE} ${IRRXML_CMAKE_PROJECT_CONFIG_FILE}
    DESTINATION ${IRRXML_CMAKE_CONFIG_DESTINATION}
    )

# Install cmake targets files (IRRXMLTargets.cmake and IRRXMLTargets-debug.cmake).
install(
    EXPORT ${IRRXML_CMAKE_TARGETS_EXPORT_NAME}
    NAMESPACE ${IRRXML_CMAKE_TARGETS_NAMESPACE}
    DESTINATION ${IRRXML_CMAKE_CONFIG_DESTINATION}
    )

#=======================================
#                INSTALL                
#=======================================

# Install the library.
install(
	FILES ${IRRXML_HEADER_FILES} 
	DESTINATION ${IRRXML_INCLUDES_DESTINATION}
	)

install(
	TARGETS ${IRRXML_TARGET_NAME}
	EXPORT ${IRRXML_CMAKE_TARGETS_EXPORT_NAME}
	RUNTIME DESTINATION ${IRRXML_RUNTIME_DESTINATION}
	LIBRARY DESTINATION ${IRRXML_LIBRARY_DESTINATION}
	ARCHIVE DESTINATION ${IRRXML_ARCHIVE_DESTINATION}
	)