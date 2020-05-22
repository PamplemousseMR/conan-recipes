from conans import ConanFile, tools, CMake
import os
import shutil


class ZZipConan(ConanFile):
    name = "zzip"
    version = "0.13.69"
    description = "The ZZIPlib provides read access on ZIP-archives and unpacked data. It features an additional simplified API following the standard Posix API for file access"
    homepage = "https://github.com/gdraheim/zziplib"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "LGPL"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }
    exports_sources = [
        os.path.join("patches", "CMakeLists.txt"),
        os.path.join("patches", "_config.h.cmake"),
        os.path.join("patches", "fseeko.h.patch")
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

    def requirements(self):
        self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version),
                  sha256="846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544")
        os.rename("{0}lib-{1}".format(self.name, self.version), self._source_folder)
        for export_source in self.exports_sources:
            shutil.copy(export_source, self._source_folder)

    def build(self):
        # Patch fseeko.h
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources[2], strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["cmake_find_package"] = "ZZip"
        self.cpp_info.names["cmake_find_package_multi"] = "ZZip"
