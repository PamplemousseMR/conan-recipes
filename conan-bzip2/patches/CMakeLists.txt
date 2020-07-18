#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project(BZip2 VERSION 1.0 LANGUAGES C)

#=======================================
#                SETTINGS               
#=======================================

set(BZIP2_TARGET_NAME "bz2")

# Set the C standard.
set(CMAKE_C_STANDARD_REQUIRED ON)
set(C_STANDARD 11)

# Export all symbols on Windows.
if(MSVC OR MSVC90 OR MSVC10)
  set(MSVC ON)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Set standard installation directories.
set(BZIP2_RUNTIME_DESTINATION "bin")
set(BZIP2_LIBRARY_DESTINATION "lib")
set(BZIP2_ARCHIVE_DESTINATION "lib")
set(BZIP2_INCLUDES_DESTINATION "include")

# Set CMake targets name, namespace and install directory.
set(BZIP2_CMAKE_TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(BZIP2_CMAKE_TARGETS_NAMESPACE "${PROJECT_NAME}::")

# CMake config files name.
set(BZIP2_CMAKE_VERSION_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(BZIP2_CMAKE_PROJECT_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake")

# CMake config files destination.
if(WIN32 AND NOT CYGWIN)
    set(BZIP2_CMAKE_CONFIG_DESTINATION "CMake")
else()
    set(BZIP2_CMAKE_CONFIG_DESTINATION "${BZIP2_LIBRARY_DESTINATION}/cmake/${PROJECT_NAME}")
endif()

#=======================================
#                 OPTION                
#=======================================

option(BZIP2_BUILD_EXE OFF)

#=======================================
#                LIBRARY                
#=======================================

# Store header files.
set(
    BZIP2_HEADER_FILES
    "bzlib.h"
    "bzlib_private.h"
    )

# Create the library (headers are here since some IDE need them here).
add_library(
    ${BZIP2_TARGET_NAME} 
    "blocksort.c"
    "bzlib.c"
    "compress.c"
    "crctable.c"
    "decompress.c"
    "huffman.c"
    "randtable.c"
    ${BZIP2_HEADER_FILES}
    )

# Export all symbols on Windows.
if(MSVC OR MSVC90 OR MSVC10)
  set_target_properties(${BZIP2_TARGET_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()


# Add include directory (includes may not be at the same place between build and install).
target_include_directories(
    ${BZIP2_TARGET_NAME}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${BZIP2_INCLUDES_DESTINATION}>
)

#=======================================
#               EXECUTABLE              
#=======================================

if(BZIP2_BUILD_EXE)
    add_executable(${CMAKE_PROJECT_NAME} "bzip2.c")
    target_link_libraries(${CMAKE_PROJECT_NAME} ${BZIP2_TARGET_NAME})
endif(BZIP2_BUILD_EXE)

#=======================================
#                CONFIG                 
#=======================================

# Include write_basic_package_version_file and configure_package_config_file.
include(CMakePackageConfigHelpers)

# Generate basic config version files (BZip2ConfigVersion.cmake).
write_basic_package_version_file(
    ${BZIP2_CMAKE_VERSION_CONFIG_FILE} 
    VERSION ${PROJECT_VERSION} 
    COMPATIBILITY SameMajorVersion
)

# Configure the config.cmake.in
configure_package_config_file(
    "${CMAKE_SOURCE_DIR}/BZip2Config.cmake.in" ${BZIP2_CMAKE_PROJECT_CONFIG_FILE} 
    INSTALL_DESTINATION  ${BZIP2_CMAKE_CONFIG_DESTINATION}
    PATH_VARS BZIP2_INCLUDES_DESTINATION BZIP2_CMAKE_CONFIG_DESTINATION BZIP2_TARGET_NAME BZIP2_LIBRARY_DESTINATION
    )

# Install cmake config files (BZIP2ConfigVersion.cmake and BZip2Config.cmake).
install(
    FILES ${BZIP2_CMAKE_VERSION_CONFIG_FILE} ${BZIP2_CMAKE_PROJECT_CONFIG_FILE}
    DESTINATION ${BZIP2_CMAKE_CONFIG_DESTINATION}
    )

# Install cmake targets files (BZIP2Targets.cmake and BZIP2Targets-debug.cmake).
install(
    EXPORT ${BZIP2_CMAKE_TARGETS_EXPORT_NAME}
    NAMESPACE ${BZIP2_CMAKE_TARGETS_NAMESPACE}
    DESTINATION ${BZIP2_CMAKE_CONFIG_DESTINATION}
    )

#=======================================
#                INSTALL                
#=======================================

# Install the library.
install(
    FILES "bzlib.h" 
    DESTINATION ${BZIP2_INCLUDES_DESTINATION}
    )

install(
    TARGETS ${BZIP2_TARGET_NAME}
    EXPORT ${BZIP2_CMAKE_TARGETS_EXPORT_NAME}
    RUNTIME DESTINATION ${BZIP2_RUNTIME_DESTINATION}
    LIBRARY DESTINATION ${BZIP2_LIBRARY_DESTINATION}
    ARCHIVE DESTINATION ${BZIP2_ARCHIVE_DESTINATION}
    )

if(BZIP2_BUILD_EXE)
    install(
        TARGETS ${CMAKE_PROJECT_NAME}
        RUNTIME DESTINATION ${BZIP2_RUNTIME_DESTINATION}
        LIBRARY DESTINATION ${BZIP2_LIBRARY_DESTINATION}
        ARCHIVE DESTINATION ${BZIP2_ARCHIVE_DESTINATION}
        )
endif(BZIP2_BUILD_EXE)