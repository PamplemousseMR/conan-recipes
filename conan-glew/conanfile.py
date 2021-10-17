import os
from conans import ConanFile, tools, CMake

class GlewConan(ConanFile):
    name = "glew"
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
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmakeFile = os.path.join(self._source_folder, "build", "cmake")
        cmake = CMake(self)
        cmake.definitions["BUILD_UTILS"] = False
        cmake.configure(source_folder=cmakeFile, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE.txt", src=self._source_folder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # Name of the find package file: findGLEW.cmake
        self.cpp_info.filenames["cmake_find_package"] = "GLEW"
        self.cpp_info.filenames["cmake_find_package_multi"] = "GLEW"

        # name of the target: GLEW::glew or GLEW::glew_s
        self.cpp_info.name = "GLEW"
        if self.options.shared:
            self.cpp_info.components["target"].name = "glew"
        else:
            self.cpp_info.components["target"].name = "glew_s"

        # Libraries
        self.cpp_info.components["target"].libs = tools.collect_libs(self)
        
        if not self.options.shared:
            self.cpp_info.defines.append("GLEW_USE_STATIC_LIBS")

        # Set the package folder as CMAKE_PREFIX_PATH to find glew-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
