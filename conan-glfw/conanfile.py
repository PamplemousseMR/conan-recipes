from conans import ConanFile, tools, CMake
import os

class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.3.2"
    description = "A multi-platform library for OpenGL, OpenGL ES, Vulkan, window and input https://www.glfw.org/"
    homepage = "https://github.com/glfw/glfw"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Zlib"
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
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256="98768e12e615fbe9f3386f5bbfeb91b5a3b45a8c4c77159cef06b1f6ff749537")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
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
            self.cpp_info.libs.extend(['Xi', 'dl', 'X11', 'pthread'])
        elif tools.os_info.is_macos:
            self.cpp_info.frameworks.extend(["Cocoa", "IOKit", "CoreVideo"])