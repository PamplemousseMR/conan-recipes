#=======================================
#                PROJECT                
#=======================================

cmake_minimum_required(VERSION 3.0)
project(zziplib VERSION 1.2.11 LANGUAGES C)

#=======================================
#                SETTINGS               
#=======================================

set(ZZIP_NAME "zzip")
set(ZZIPFSEEKO_NAME "zzipfseeko")

# Set the C standard.
set(CMAKE_C_STANDARD_REQUIRED ON)
set(C_STANDARD 11)

# Set standard installation directories.
set(ZZIPLIB_RUNTIME_DESTINATION "bin")
set(ZZIPLIB_LIBRARY_DESTINATION "lib")
set(ZZIPLIB_ARCHIVE_DESTINATION "lib")
set(ZZIPLIB_INCLUDES_DIR "include")
set(ZZIPLIB_INCLUDES_DESTINATION "${ZZIPLIB_INCLUDES_DIR}/${ZZIP_NAME}")

#=======================================
#                 INIT                 
#=======================================

include(CheckIncludeFiles)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckTypeSize)
include(TestBigEndian)

set(ZZIP_HAVE_ZLIB_H 1)

if(NOT ANDROID)
    check_include_files(dirent.h ZZIP_HAVE_DIRENT_H)
endif()

check_include_files(byteswap.h ZZIP_HAVE_BYTESWAP_H)
check_include_files(direct.h ZZIP_HAVE_DIRECT_H)
check_include_files(dlfcn.h ZZIP_HAVE_DLFCN_H)
check_include_files(fnmatch.h ZZIP_HAVE_FNMATCH_H)
check_include_files(inttypes.h ZZIP_HAVE_INTTYPES_H)
check_include_files(io.h ZZIP_HAVE_IO_H)
check_include_files(memory.h ZZIP_HAVE_MEMORY_H)
check_include_files(ndir.h ZZIP_HAVE_NDIR_H)
check_include_files(stdint.h ZZIP_HAVE_STDINT_H)
check_include_files(stdlib.h ZZIP_HAVE_STDLIB_H)
check_include_files(strings.h ZZIP_HAVE_STRINGS_H)
check_include_files(string.h ZZIP_HAVE_STRING_H)
check_include_files("sys/dir.h" ZZIP_HAVE_SYS_DIR_H)
check_include_files("sys/int_types.h" ZZIP_HAVE_SYS_INT_TYPES_H)
check_include_files("sys/mman.h" ZZIP_HAVE_SYS_MMAN_H)
check_include_files("sys/ndir.h" ZZIP_HAVE_SYS_NDIR_H)
check_include_files("sys/param.h" ZZIP_HAVE_SYS_PARAM_H)
check_include_files("sys/stat.h" ZZIP_HAVE_SYS_STAT_H)
check_include_files("sys/types.h" ZZIP_HAVE_SYS_TYPES_H)
check_include_files(unistd.h ZZIP_HAVE_UNISTD_H)
check_include_files(winbase.h ZZIP_HAVE_WINBASE_H)
check_include_files(windows.h ZZIP_HAVE_WINDOWS_H)
check_include_files(winnt.h ZZIP_HAVE_WINNT_H)
check_include_files("stdlib.h;stdarg.h;string.h;float.h" ZZIP_STDC_HEADERS)

check_function_exists(strcasecmp ZZIP_HAVE_STRCASECMP)
check_function_exists(strndup ZZIP_HAVE_STRNDUP)

check_type_size(int ZZIP_SIZEOF_INT)
check_type_size(long ZZIP_SIZEOF_LONG)
check_type_size(short ZZIP_SIZEOF_SHORT)

test_big_endian(ZZIP_WORDS_BIGENDIAN)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/_config.h.cmake ${CMAKE_CURRENT_SOURCE_DIR}/zzip/_config.h)
add_definitions(-DHAVE_CONFIG_H)

#=======================================
#              LIBRARY ZZip             
#=======================================

if(BUILD_SHARED_LIBS)
    add_definitions(-DZZIP_EXPORTS)
endif()

# Store header files.
set(
    ZZIP_HEADER_FILES
    zzip/zzip.h
    zzip/types.h
    zzip/conf.h 
    zzip/_msvc.h 
    zzip/plugin.h 
    zzip/fetch.h
    ${CMAKE_CURRENT_SOURCE_DIR}/zzip/_config.h
    )

# Create the library (headers are here since some IDE need them here).
add_library(
    ${ZZIP_NAME} 
    zzip/dir.c
    zzip/err.c 
    zzip/file.c 
    zzip/info.c 
    zzip/plugin.c 
    zzip/stat.c
    zzip/write.c 
    zzip/zip.c 
    zzip/fetch.c
    ${ZZIP_HEADER_FILES}
    )

# Add include directory (includes may not be at the same place between build and install).
target_include_directories(
    ${ZZIP_NAME}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${ZZIPLIB_INCLUDES_DIR}>
)

#=======================================
#           LIBRARY ZZipFSeeko          
#=======================================

# Store header files.
set(
    ZZIPFSEEKO_HEADER_FILES
    zzip/fseeko.h
    zzip/fetch.h
    )

# Create the library (headers are here since some IDE need them here).
add_library(
    ${ZZIPFSEEKO_NAME} 
    zzip/fseeko.c 
    zzip/fetch.c
    ${ZZIPFSEEKO_HEADER_FILES}
    )

# Export all symbols on Windows.
if(MSVC OR MSVC90 OR MSVC10)
  set_target_properties(${ZZIPFSEEKO_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()


# Add include directory (includes may not be at the same place between build and install).
target_include_directories(
    ${ZZIPFSEEKO_NAME}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${ZZIPLIB_INCLUDES_DIR}>
)

#=======================================
#           LIBRARY ZZipMMapped         
#=======================================

if(NOT MSVC)
    #add_library(zzipmmapped zzip/mmapped.c zzip/memdisk.c zzip/fetch.c)
    #target_include_directories(zzipmmapped PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
endif()

#=======================================
#                PACKAGE                
#=======================================

find_package(ZLIB REQUIRED)

target_include_directories(${ZZIP_NAME} PRIVATE ${ZLIB_INCLUDE_DIRS})
target_link_libraries(${ZZIP_NAME} ${ZLIB_LIBRARIES})

target_include_directories(${ZZIPFSEEKO_NAME} PRIVATE ${ZLIB_INCLUDE_DIRS})
target_link_libraries(${ZZIPFSEEKO_NAME} ${ZLIB_LIBRARIES})

if(NOT MSVC)
    #target_include_directories(zzipmmapped PRIVATE ${ZLIB_INCLUDE_DIRS})
    #target_link_libraries(zzipmmapped ${ZLIB_LIBRARIES})
endif()

#=======================================
#                INSTALL                
#=======================================

# Install the zzip.
install(
    FILES ${ZZIP_HEADER_FILES} 
    DESTINATION ${ZZIPLIB_INCLUDES_DESTINATION}
    )

install(
    TARGETS ${ZZIP_NAME}
    RUNTIME DESTINATION ${ZZIPLIB_RUNTIME_DESTINATION}
    LIBRARY DESTINATION ${ZZIPLIB_LIBRARY_DESTINATION}
    ARCHIVE DESTINATION ${ZZIPLIB_ARCHIVE_DESTINATION}
    )

# Install the zzipfseeko.
install(
    FILES ${ZZIPFSEEKO_HEADER_FILES} 
    DESTINATION ${ZZIPLIB_INCLUDES_DESTINATION}
    )

install(
    TARGETS ${ZZIPFSEEKO_NAME}
    RUNTIME DESTINATION ${ZZIPLIB_RUNTIME_DESTINATION}
    LIBRARY DESTINATION ${ZZIPLIB_LIBRARY_DESTINATION}
    ARCHIVE DESTINATION ${ZZIPLIB_ARCHIVE_DESTINATION}
    )