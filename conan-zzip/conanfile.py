import os
import shutil
from conans import ConanFile, tools, CMake

class ZZipConan(ConanFile):
    name = "zzip"
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
    exports_sources = [
        "CMakeLists.txt",
        os.path.join("patches", "CMakeLists.txt"),
        os.path.join("patches", "_config.h.cmake"),
        os.path.join("patches", "fseeko.h.patch")
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

    def requirements(self):
        for requirement in self.conan_data["requirements"][self.version]:
            self.requires.add("{0}@{1}/{2}".format(requirement, self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}lib-{1}".format(self.name, self.version), self._source_folder)
        for export_source in self.conan_data["export_sources"][self.version]:
            shutil.copy(os.path.join("patches", export_source), self._source_folder)

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(base_path=self._source_folder, patch_file=os.path.join("patches", patch), strip=0)
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copy the license file.
        self.copy("COPYING.LIB", src=self._source_folder, dst="licenses", keep_path=False)

        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Set the name of conan auto generated FindZZip.cmake.
        self.cpp_info.name = "ZZip"

        self.cpp_info.libs = tools.collect_libs(self)

