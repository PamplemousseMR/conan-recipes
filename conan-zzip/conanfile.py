from conans import ConanFile, tools, CMake
import os
import shutil

class ZzipConan(ConanFile):
    name = "zzip"
    version = "0.13.69"
    description = "The ZZIPlib provides read access on ZIP-archives and unpacked data. It features an additional simplified API following the standard Posix API for file access"
    homepage = "https://github.com/gdraheim/zziplib"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "LGPL"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }
    exports = "LICENSE.md"
    exports_sources = [
        os.path.join("patches", "CMakeLists.txt"), 
        os.path.join("patches", "WrappedCMakeLists.txt"),
        os.path.join("patches", "_config.h.cmake")
    ]
    short_paths=True
    
    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        
    def requirements(self):
        if tools.os_info.is_windows:
            self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256="846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544")
        os.rename("{0}lib-{1}".format(self.name, self.version), self._source_folder)
        for export_source in self.exports_sources:
            shutil.copy(export_source, self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ZZIP_CONAN_INFO_DIR"] = self.build_folder
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)        
        for export in self.exports:
            self.copy(export, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["cmake_find_package"] = "ZZip"
        self.cpp_info.names["cmake_find_package_multi"] = "ZZip"