import os
import shutil
from conans import ConanFile, tools, CMake

class Bzip2Conan(ConanFile):
    name = "bzip2"
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

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        git = tools.Git(folder=self._source_folder)
        git.clone(**self.conan_data["sources"][self.version])
        os.rename("{0}_sources".format(self.name), self._source_folder)
        git.checkout(self.conan_data["commit"][self.version])
        for export_source in self.conan_data["export_sources"][self.version]:
            shutil.copy(os.path.join("patches", export_source), self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BZIP2_BUILD_EXE"] = self.options.build_exe
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE", src=self._source_folder, dst="licenses", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Name of the find package file: findBZip2.cmake
        self.cpp_info.filenames["cmake_find_package"] = "BZip2"
        self.cpp_info.filenames["cmake_find_package_multi"] = "BZip2"

        # name of the target: BZip2::bz2
        self.cpp_info.name = "BZip2"
        self.cpp_info.components["bz2"].name = "bz2"

        # Libraries
        self.cpp_info.components["bz2"].libs = tools.collect_libs(self)

        # Set the package folder as CMAKE_PREFIX_PATH to find BZip2Config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
