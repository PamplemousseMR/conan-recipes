import os
import shutil
from conans import ConanFile, tools, CMake


class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.8"
    description = "bzip2 is a free and open-source file compression program that uses the Burrows-Wheeler algorithm"
    homepage = "https://sourceware.org/pub/bzip2"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "bzip2"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_exe": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "build_exe": False
    }
    exports_sources = [
        os.path.join("patches", "CMakeLists.txt"),
        os.path.join("patches", "BZip2Config.cmake.in")
    ]
    short_paths = True

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get("{0}/{1}-{2}.tar.gz".format(self.homepage, self.name, self.version),
                  sha256="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
        for export_source in self.exports_sources:
            shutil.copy(export_source, self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BZIP2_BUILD_EXE"] = self.options.build_exe
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindBZip2.cmake.
        self.cpp_info.names["cmake_find_package"] = "BZip2"
        self.cpp_info.names["cmake_find_package_multi"] = "BZip2"

        # Set the package folder as CMAKE_PREFIX_PATH to find BZip2Config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
