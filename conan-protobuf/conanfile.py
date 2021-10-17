import os
import shutil
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

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

            if self.settings.os == "Windows" and self.settings.compiler in ["Visual Studio", "clang"] and "MT" in self.settings.compiler.runtime:
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
        # Name of the find package file: findProtobuf.cmake
        self.cpp_info.filenames["cmake_find_package"] = "Protobuf"
        self.cpp_info.filenames["cmake_find_package_multi"] = "Protobuf"

        # Name of the target: protobuf::
        self.cpp_info.name = "protobuf"
        self.cpp_info.names["pkg_config"] = "protobuf_full_package" # unofficial, but required to avoid side effects (libprotobuf component "steals" the default global pkg_config name)
        
        lib_prefix = "lib" if self.settings.compiler == "Visual Studio" else ""
        lib_suffix = "d" if self.settings.build_type == "Debug" else ""

        # Create the target: protobuf::libprotobuf
        self.cpp_info.components["libprotobuf"].name = "libprotobuf"
        self.cpp_info.components["libprotobuf"].names["pkg_config"] = "protobuf"
        self.cpp_info.components["libprotobuf"].libs = [lib_prefix + "protobuf" + lib_suffix]
        if self.settings.os == "Linux":
            self.cpp_info.components["libprotobuf"].system_libs.append("pthread")
            if (self.settings.compiler == "clang" and self.settings.arch == "x86") or "arm" in str(self.settings.arch):
                self.cpp_info.components["libprotobuf"].system_libs.append("atomic")

        # Create the target: protobuf::libprotoc
        self.cpp_info.components["libprotoc"].name = "protoc"
        self.cpp_info.components["libprotoc"].libs = [lib_prefix + "protoc" + lib_suffix]
        self.cpp_info.components["libprotoc"].requires = ["libprotobuf"]

        # Create the target: protobuf::libprotobuf-lite
        if self.options.lite:
            self.cpp_info.components["libprotobuf-lite"].name = "libprotobuf-lite"
            self.cpp_info.components["libprotobuf-lite"].names["pkg_config"] = "protobuf-lite"
            self.cpp_info.components["libprotobuf-lite"].libs = [lib_prefix + "protobuf-lite" + lib_suffix]
        if self.settings.os == "Linux":
                self.cpp_info.components["libprotobuf-lite"].system_libs.append("pthread")
                if (self.settings.compiler == "clang" and self.settings.arch == "x86") or "arm" in str(self.settings.arch):
                    self.cpp_info.components["libprotobuf-lite"].system_libs.append("atomic")

        # Set the package folder as CMAKE_PREFIX_PATH to find protobuf-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)