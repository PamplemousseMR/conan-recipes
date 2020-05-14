from conans import ConanFile, tools, CMake
import os
import shutil

class GlewConan(ConanFile):
    name = "glew"
    version = "2.1.0"
    description = "The OpenGL Extension Wrangler Library"
    homepage = "https://github.com/nigels-com/glew"
    url = "https://github.com/PamplemousseMR/conan-glew"
    license = "MIT"
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
        del self.settings.compiler.cppstd
        
    def source(self):
        tools.get("{0}/releases/download/{1}-{2}/{1}-{2}.tgz".format(self.homepage, self.name, self.version), sha256="04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
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
        if tools.os_info.is_windows:
            if not self.options.shared:
                self.cpp_info.defines.append("GLEW_STATIC")
                self.cpp_info.libs.append('opengl32')
        elif tools.os_info.is_linux:
            if not self.options.shared:
                self.cpp_info.libs.append('GL')
        elif tools.os_info.is_macos:
            self.cpp_info.sharedlinkflags.append("-framework OpenGL")