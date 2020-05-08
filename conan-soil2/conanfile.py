from conans import ConanFile, tools, CMake
import os
import shutil

class Soil2Conan(ConanFile):
    name = "soil2"
    version = "1.11"
    description = "Simple OpenGL Image Library"
    homepage = "https://github.com/SpartanJ/SOIL2"
    url = "https://github.com/PamplemousseMR/conan-bzp2"
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
        tools.get("{0}/archive/release-{1}.tar.gz".format(self.homepage, self.version), sha256="104a2de5bb74b58b7b7cda7592b174d9aa0585eeb73d0bec4901f419321358bc")
        os.rename("SOIL2-release-{0}".format(self.version), self._source_folder)
        shutil.copy(self.exports_sources, self._source_folder)

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
        if tools.os_info.is_linux:
            self.cpp_info.libs.append('GL')
        elif tools.os_info.is_macos:
            self.cpp_info.sharedlinkflags.append("-framework OpenGL -framework CoreFoundation")
        elif tools.os_info.is_windows:
            self.cpp_info.libs.append('opengl32')