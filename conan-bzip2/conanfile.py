from conans import ConanFile, tools, CMake
import os
import shutil

class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.8"
    description = "bzip2 is a free and open-source file compression program that uses the Burrows-Wheeler algorithm"
    homepage = "https://sourceware.org/pub/bzip2"
    url = "https://github.com/PamplemousseMR/conan-bzip2"
    license = "bzip2"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
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
    exports = "LICENSE.md"
    exports_sources = os.path.join("patches", "CMakeLists.txt")
    short_paths=True
    
    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("{0}/{1}-{2}.tar.gz".format(self.homepage, self.name, self.version), sha256="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
        shutil.copy(self.exports_sources, self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BZIP2_BUILD_EXE"] = self.options.build_exe
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)        
        for export in self.exports:
            self.copy(export, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)