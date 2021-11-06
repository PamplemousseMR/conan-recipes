import os
import shutil
import textwrap
from conans import ConanFile, tools, CMake

class ProtobufConan(ConanFile):
    name = "protobuf"
    description = "Protocol Buffers - Google's data interchange format"
    homepage = "https://github.com/protocolbuffers/protobuf"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_zlib": [True, False],
        "with_rtti": [True, False],
        "lite": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_zlib": False,
        "with_rtti": True,
        "lite": True,
    }
    exports_sources = [
        "CMakeLists.txt",
        os.path.join("patches", "protobuf-config.cmake.patch")
    ]
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    @property
    def _module_subfolder(self):
        return os.path.join("lib", "cmake")

    @property
    def _module_file(self):
        return "conan-{}-targets.cmake".format(self.name)  

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

            if tools.os_info.is_windows and self.settings.compiler in ["Visual Studio", "clang"] and "MT" in self.settings.compiler.runtime:
                raise ConanInvalidConfiguration("Protobuf can't be built with shared + MT(d) runtimes")

            if tools.is_apple_os(self.settings.os):
                raise ConanInvalidConfiguration("Protobuf could not be built as shared library for Mac.")

        if self.settings.compiler == "Visual Studio":
            if tools.Version(self.settings.compiler.version) < "14":
                raise ConanInvalidConfiguration("On Windows Protobuf can only be built with Visual Studio 2015 or higher.")

    def requirements(self):
        if self.options.with_zlib:
            self.requires.add("zlib/{0}@{1}/{2}".format(self.conan_data["zlib"][self.version], self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        if self.conan_data["patches"][self.version]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(base_path=self._source_folder, patch_file=os.path.join("patches", patch), strip=0)
        cmake = CMake(self)
        cmake.definitions["protobuf_WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["protobuf_BUILD_TESTS"] = False
        cmake.definitions["protobuf_BUILD_PROTOC_BINARIES"] = True
        if tools.Version(self.version) >= "3.14.0":
                cmake.definitions["protobuf_BUILD_LIBPROTOC"] = True
        if tools.Version(self.version) >= "3.15.4":
                cmake.definitions["protobuf_DISABLE_RTTI"] = not self.options.with_rtti
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["protobuf_MSVC_STATIC_RUNTIME"] = "MT" in str(self.settings.compiler.runtime)
        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE", src=self._source_folder, dst="licenses", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

        if not self.options.lite:
            tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), "libprotobuf-lite.*")
            tools.remove_files_by_mask(os.path.join(self.package_folder, "bin"), "libprotobuf-lite.*")

    def package_info(self):
        # Name of the find package file: Findprotobuf.cmake
        self.cpp_info.filenames["cmake_find_package"] = "protobuf"
        self.cpp_info.filenames["cmake_find_package_multi"] = "protobuf"

        # Name of the target: protobuf::
        self.cpp_info.name = "protobuf"
        self.cpp_info.names["pkg_config"] = "protobuf_full_package" # unofficial, but required to avoid side effects (libprotobuf component "steals" the default global pkg_config name)
        
        lib_suffix = "d" if self.settings.build_type == "Debug" else ""

        # Create custom target: protobuf_generate
        content = textwrap.dedent("""\
                    function(protobuf_generate)
                      include(CMakeParseArguments)

                      set(_options APPEND_PATH)
                      set(_singleargs LANGUAGE OUT_VAR EXPORT_MACRO PROTOC_OUT_DIR PLUGIN)
                      if(COMMAND target_sources)
                        list(APPEND _singleargs TARGET)
                      endif()
                      set(_multiargs PROTOS IMPORT_DIRS GENERATE_EXTENSIONS PROTOC_OPTIONS)

                      cmake_parse_arguments(protobuf_generate "${_options}" "${_singleargs}" "${_multiargs}" "${ARGN}")

                      if(NOT protobuf_generate_PROTOS AND NOT protobuf_generate_TARGET)
                        message(SEND_ERROR "Error: protobuf_generate called without any targets or source files")
                        return()
                      endif()

                      if(NOT protobuf_generate_OUT_VAR AND NOT protobuf_generate_TARGET)
                        message(SEND_ERROR "Error: protobuf_generate called without a target or output variable")
                        return()
                      endif()

                      if(NOT protobuf_generate_LANGUAGE)
                        set(protobuf_generate_LANGUAGE cpp)
                      endif()
                      string(TOLOWER ${protobuf_generate_LANGUAGE} protobuf_generate_LANGUAGE)

                      if(NOT protobuf_generate_PROTOC_OUT_DIR)
                        set(protobuf_generate_PROTOC_OUT_DIR ${CMAKE_CURRENT_BINARY_DIR})
                      endif()

                      if(protobuf_generate_EXPORT_MACRO AND protobuf_generate_LANGUAGE STREQUAL cpp)
                        set(_dll_export_decl "dllexport_decl=${protobuf_generate_EXPORT_MACRO}:")
                      endif()
                      
                      if(protobuf_generate_PLUGIN)
                          set(_plugin "--plugin=${protobuf_generate_PLUGIN}")
                      endif()

                      if(NOT protobuf_generate_GENERATE_EXTENSIONS)
                        if(protobuf_generate_LANGUAGE STREQUAL cpp)
                          set(protobuf_generate_GENERATE_EXTENSIONS .pb.h .pb.cc)
                        elseif(protobuf_generate_LANGUAGE STREQUAL python)
                          set(protobuf_generate_GENERATE_EXTENSIONS _pb2.py)
                        else()
                          message(SEND_ERROR "Error: protobuf_generate given unknown Language ${LANGUAGE}, please provide a value for GENERATE_EXTENSIONS")
                          return()
                        endif()
                      endif()

                      if(protobuf_generate_TARGET)
                        get_target_property(_source_list ${protobuf_generate_TARGET} SOURCES)
                        foreach(_file ${_source_list})
                          if(_file MATCHES "proto$")
                            list(APPEND protobuf_generate_PROTOS ${_file})
                          endif()
                        endforeach()
                      endif()

                      if(NOT protobuf_generate_PROTOS)
                        message(SEND_ERROR "Error: protobuf_generate could not find any .proto files")
                        return()
                      endif()

                      if(protobuf_generate_APPEND_PATH)
                        # Create an include path for each file specified
                        foreach(_file ${protobuf_generate_PROTOS})
                          get_filename_component(_abs_file ${_file} ABSOLUTE)
                          get_filename_component(_abs_path ${_abs_file} PATH)
                          list(FIND _protobuf_include_path ${_abs_path} _contains_already)
                          if(${_contains_already} EQUAL -1)
                              list(APPEND _protobuf_include_path -I ${_abs_path})
                          endif()
                        endforeach()
                      endif()

                      foreach(DIR ${protobuf_generate_IMPORT_DIRS})
                        get_filename_component(ABS_PATH ${DIR} ABSOLUTE)
                        list(FIND _protobuf_include_path ${ABS_PATH} _contains_already)
                        if(${_contains_already} EQUAL -1)
                            list(APPEND _protobuf_include_path -I ${ABS_PATH})
                        endif()
                      endforeach()

                      if(NOT _protobuf_include_path)
                        set(_protobuf_include_path -I ${CMAKE_CURRENT_SOURCE_DIR})
                      endif()

                      set(_generated_srcs_all)
                      foreach(_proto ${protobuf_generate_PROTOS})
                        get_filename_component(_abs_file ${_proto} ABSOLUTE)
                        get_filename_component(_abs_dir ${_abs_file} DIRECTORY)

                        get_filename_component(_file_full_name ${_proto} NAME)
                        string(FIND "${_file_full_name}" "." _file_last_ext_pos REVERSE)
                        string(SUBSTRING "${_file_full_name}" 0 ${_file_last_ext_pos} _basename)

                        set(_suitable_include_found FALSE)
                        foreach(DIR ${_protobuf_include_path})
                          if(NOT DIR STREQUAL "-I")
                            file(RELATIVE_PATH _rel_dir ${DIR} ${_abs_dir})
                            string(FIND "${_rel_dir}" "../" _is_in_parent_folder)
                            if (NOT ${_is_in_parent_folder} EQUAL 0)
                              set(_suitable_include_found TRUE)
                              break()
                            endif()
                          endif()
                        endforeach()

                        if(NOT _suitable_include_found)
                          message(SEND_ERROR "Error: protobuf_generate could not find any correct proto include directory.")
                          return()
                        endif()

                        set(_generated_srcs)
                        foreach(_ext ${protobuf_generate_GENERATE_EXTENSIONS})
                          list(APPEND _generated_srcs "${protobuf_generate_PROTOC_OUT_DIR}/${_rel_dir}/${_basename}${_ext}")
                        endforeach()
                        list(APPEND _generated_srcs_all ${_generated_srcs})

                        add_custom_command(
                          OUTPUT ${_generated_srcs}
                          COMMAND  protobuf::protoc
                          ARGS ${protobuf_generate_PROTOC_OPTIONS} --${protobuf_generate_LANGUAGE}_out ${_dll_export_decl}${protobuf_generate_PROTOC_OUT_DIR} ${_plugin} ${_protobuf_include_path} ${_abs_file}
                          DEPENDS ${_abs_file} protobuf::protoc
                          COMMENT "Running ${protobuf_generate_LANGUAGE} protocol buffer compiler on ${_proto}. Custom options: ${protobuf_generate_PROTOC_OPTIONS}"
                          VERBATIM )
                      endforeach()

                      set_source_files_properties(${_generated_srcs_all} PROPERTIES GENERATED TRUE)
                      if(protobuf_generate_OUT_VAR)
                        set(${protobuf_generate_OUT_VAR} ${_generated_srcs_all} PARENT_SCOPE)
                      endif()
                      if(protobuf_generate_TARGET)
                        target_sources(${protobuf_generate_TARGET} PRIVATE ${_generated_srcs_all})
                      endif()

                    endfunction()
            """)
        tools.save(os.path.join(self.package_folder, self._module_subfolder, self._module_file), content)
        module_rel_path = os.path.join(self._module_subfolder, self._module_file)

        # Create the target: protobuf::libprotobuf
        self.cpp_info.components["libprotobuf"].name = "libprotobuf"
        self.cpp_info.components["libprotobuf"].names["pkg_config"] = "protobuf"
        self.cpp_info.components["libprotobuf"].libs = ["libprotobuf" + lib_suffix]
        self.cpp_info.components["libprotobuf"].builddirs.append(self._module_subfolder)
        self.cpp_info.components["libprotobuf"].build_modules["cmake_find_package"] = [module_rel_path]
        self.cpp_info.components["libprotobuf"].build_modules["cmake_find_package_multi"] = [module_rel_path]
        if tools.os_info.is_linux:
            self.cpp_info.components["libprotobuf"].system_libs.append("pthread")
            if (self.settings.compiler == "clang" and self.settings.arch == "x86") or "arm" in str(self.settings.arch):
                self.cpp_info.components["libprotobuf"].system_libs.append("atomic")

        # Create the target: protobuf::libprotoc
        self.cpp_info.components["libprotoc"].name = "protoc"
        self.cpp_info.components["libprotoc"].libs = ["libprotoc" + lib_suffix]
        self.cpp_info.components["libprotoc"].requires = ["libprotobuf"]
        self.cpp_info.components["libprotoc"].builddirs.append(self._module_subfolder)
        self.cpp_info.components["libprotoc"].build_modules["cmake_find_package"] = [module_rel_path]
        self.cpp_info.components["libprotoc"].build_modules["cmake_find_package_multi"] = [module_rel_path]

        # Create the target: protobuf::libprotobuf-lite
        if self.options.lite:
            self.cpp_info.components["libprotobuf-lite"].name = "libprotobuf-lite"
            self.cpp_info.components["libprotobuf-lite"].names["pkg_config"] = "protobuf-lite"
            self.cpp_info.components["libprotobuf-lite"].libs = ["libprotobuf-lite" + lib_suffix]
            self.cpp_info.components["libprotobuf-lite"].builddirs.append(self._module_subfolder)
            self.cpp_info.components["libprotobuf-lite"].build_modules["cmake_find_package"] = [module_rel_path]
            self.cpp_info.components["libprotobuf-lite"].build_modules["cmake_find_package_multi"] = [module_rel_path]
            if tools.os_info.is_linux:
                self.cpp_info.components["libprotobuf-lite"].system_libs.append("pthread")
                if (self.settings.compiler == "clang" and self.settings.arch == "x86") or "arm" in str(self.settings.arch):
                    self.cpp_info.components["libprotobuf-lite"].system_libs.append("atomic")

        # Set the package folder as CMAKE_PREFIX_PATH to find protobuf-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)