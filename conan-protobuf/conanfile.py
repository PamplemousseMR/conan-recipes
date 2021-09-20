import os
import shutil
from conans import ConanFile, tools, CMake


class ProtobufConan(ConanFile):
    name = "protobuf"
    description = "Protocol Buffers - Google's data interchange format"
    homepage = "https://github.com/protocolbuffers/protobuf"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_zlib": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_zlib": False
    }
    exports_sources = os.path.join("patches", "protobuf-config.cmake.patch")
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
        cmake.definitions["protobuf_BUILD_LIBPROTOC"] = True
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["protobuf_MSVC_STATIC_RUNTIME"] = "MT" in str(self.settings.compiler.runtime)
        cmake.configure(source_folder=os.path.join(self._source_folder, "cmake"), build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE", src=self._source_folder, dst="licenses", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # The module name is Protobuf while the config name is protobuf.
        self.cpp_info.filenames["cmake_find_package"] = "Protobuf"
        self.cpp_info.filenames["cmake_find_package_multi"] = "protobuf"

        # Set the name of conan auto generated FindProtobuf.cmake.
        self.cpp_info.names["cmake_find_package"] = "protobuf"
        self.cpp_info.names["cmake_find_package_multi"] = "protobuf"

        # Set the package folder as CMAKE_PREFIX_PATH to find protobuf-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
