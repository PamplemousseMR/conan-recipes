import os
from conans import ConanFile, tools, CMake


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    description = "A massively spiffy yet delicately unobtrusive compression library. http://zlib.net/"
    homepage = "https://github.com/madler/zlib"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Zlib"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    exports_sources = os.path.join("patches", "CMakeLists.txt.patch")
    short_paths = True

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version),
                  sha256="629380c90a77b964d896ed37163f5c3a34f6e6d897311f1df2a7016355c45eff")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources, strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["cmake_find_package"] = "ZLIB"
        self.cpp_info.names["cmake_find_package_multi"] = "ZLIB"
