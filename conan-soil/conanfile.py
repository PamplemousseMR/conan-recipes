from conans import ConanFile, tools, CMake
import os
import shutil

class SoilConan(ConanFile):
    name = "soil"
    version = "1.0"
    description = "Simple OpenGL Image Library"
    homepage = "http://lonesock.net/soil.html"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Public Domain"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    exports = "LICENSE.md"
    exports_sources = [
        os.path.join("patches", "CMakeLists.txt"),
        os.path.join("patches", "SOILConfig.cmake.in")
    ]
    
    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get("http://www.lonesock.net/files/soil.zip", sha256="a2305b8d64f6d636e36d669bbdb0ca5445d1345c754b3d61d3f037dad2e5f701")
        os.rename("Simple OpenGL Image Library", self._source_folder)
        for export_source in self.exports_sources:
            shutil.copy(export_source, self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)        
        for export in self.exports:
            self.copy(export, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        # Set the name of conan auto generated FindSOIL.cmake.
        self.cpp_info.names["cmake_find_package"] = "SOIL"
        self.cpp_info.names["cmake_find_package_multi"] = "SOIL"
        # Set the package folder as CMAKE_PREFIX_PATH to find SOILConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
        if tools.os_info.is_linux:
            self.cpp_info.libs.append('GL')
        elif tools.os_info.is_macos:
            self.cpp_info.frameworks.extend(["OpenGL", "CoreFoundation"])
        elif tools.os_info.is_windows:
            self.cpp_info.libs.append('opengl32')