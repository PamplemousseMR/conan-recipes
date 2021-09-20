import os
from conans import ConanFile, tools, CMake


class ZlibConan(ConanFile):
    name = "zlib"
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

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(base_path=self._source_folder, patch_file=os.path.join("patches", patch), strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindZLIB.cmake.
        self.cpp_info.names["cmake_find_package"] = "ZLIB"
        self.cpp_info.names["cmake_find_package_multi"] = "ZLIB"
