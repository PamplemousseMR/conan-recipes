#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project(SOIL VERSION 1.0 LANGUAGES C)

#=======================================
#                SETTINGS               
#=======================================

set(SOIL_TARGET_NAME ${PROJECT_NAME})

# Set the C standard.
set(CMAKE_C_STANDARD_REQUIRED ON)
set(C_STANDARD 11)

# Export all symbols on Windows.
if(MSVC OR MSVC90 OR MSVC10)
  set(MSVC ON)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Set standard installation directories.
set(SOIL_RUNTIME_DESTINATION "bin")
set(SOIL_LIBRARY_DESTINATION "lib")
set(SOIL_ARCHIVE_DESTINATION "lib")
set(SOIL_INCLUDES_DIR "include")
set(SOIL_INCLUDES_DESTINATION "${SOIL_INCLUDES_DIR}/${PROJECT_NAME}")

# Set CMake targets name, namespace and install directory.
set(SOIL_CMAKE_TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(SOIL_CMAKE_TARGETS_NAMESPACE "${PROJECT_NAME}::")

# CMake config files name.
set(SOIL_CMAKE_VERSION_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(SOIL_CMAKE_PROJECT_CONFIG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake")

# CMake config files destination.
if(WIN32 AND NOT CYGWIN)
	set(SOIL_CMAKE_CONFIG_DESTINATION "CMake")
else()
	set(SOIL_CMAKE_CONFIG_DESTINATION "${SOIL_LIBRARY_DESTINATION}/cmake/${PROJECT_NAME}")
endif()

#=======================================
#                LIBRARY                
#=======================================

# Store header files.
set(
	SOIL_HEADER_FILES
	src/image_DXT.h
	src/image_helper.h
	src/SOIL.h
	src/stb_image_aug.h
	src/stbi_DDS_aug.h
	src/stbi_DDS_aug_c.h
	)

# Create the library (headers are here since some IDE need them here).
add_library(
	${SOIL_TARGET_NAME} 
	src/image_DXT.c
	src/image_helper.c
	src/SOIL.c
	src/stb_image_aug.c
	${SOIL_HEADER_FILES}
	)

# Add include directory (includes may not be at the same place between build and install).
target_include_directories(
    ${SOIL_TARGET_NAME}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    $<INSTALL_INTERFACE:${SOIL_INCLUDES_DIR}>
)

#=======================================
#                PACKAGE                
#=======================================

find_package(OpenGL REQUIRED)
target_link_libraries(${SOIL_TARGET_NAME} PUBLIC OpenGL::GL)

if(APPLE)
	target_link_libraries(${SOIL_TARGET_NAME} PUBLIC "-framework CoreFoundation")
endif()

#=======================================
#                CONFIG                 
#=======================================

# Include write_basic_package_version_file and configure_package_config_file.
include(CMakePackageConfigHelpers)

# Generate basic config version files (SOILConfigVersion.cmake).
write_basic_package_version_file(
    ${SOIL_CMAKE_VERSION_CONFIG_FILE} 
    VERSION ${PROJECT_VERSION} 
    COMPATIBILITY SameMajorVersion
)

# Configure the config.cmake.in
configure_package_config_file(
	"${CMAKE_SOURCE_DIR}/SOILConfig.cmake.in" ${SOIL_CMAKE_PROJECT_CONFIG_FILE} 
	INSTALL_DESTINATION  ${SOIL_CMAKE_CONFIG_DESTINATION}
	PATH_VARS SOIL_INCLUDES_DESTINATION SOIL_CMAKE_CONFIG_DESTINATION SOIL_TARGET_NAME SOIL_LIBRARY_DESTINATION
	)

# Install cmake config files (SOILConfigVersion.cmake and SOILConfig.cmake).
install(
    FILES ${SOIL_CMAKE_VERSION_CONFIG_FILE} ${SOIL_CMAKE_PROJECT_CONFIG_FILE}
    DESTINATION ${SOIL_CMAKE_CONFIG_DESTINATION}
    )

# Install cmake targets files (SOILTargets.cmake and SOILTargets-debug.cmake).
install(
    EXPORT ${SOIL_CMAKE_TARGETS_EXPORT_NAME}
    NAMESPACE ${SOIL_CMAKE_TARGETS_NAMESPACE}
    DESTINATION ${SOIL_CMAKE_CONFIG_DESTINATION}
    )

#=======================================
#                INSTALL                
#=======================================

# Install the library.
install(
	FILES ${SOIL_HEADER_FILES} 
	DESTINATION ${SOIL_INCLUDES_DESTINATION}
	)

install(
	TARGETS ${SOIL_TARGET_NAME}
	EXPORT ${SOIL_CMAKE_TARGETS_EXPORT_NAME}
	RUNTIME DESTINATION ${SOIL_RUNTIME_DESTINATION}
	LIBRARY DESTINATION ${SOIL_LIBRARY_DESTINATION}
	ARCHIVE DESTINATION ${SOIL_ARCHIVE_DESTINATION}
	)