import os
from conans import ConanFile, tools, CMake


class GlewConan(ConanFile):
    name = "glew"
    version = "2.1.0"
    description = "The OpenGL Extension Wrangler Library"
    homepage = "https://github.com/nigels-com/glew"
    url = "https://github.com/PamplemousseMR/conan-glew"
    license = "MIT"
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

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get("{0}/releases/download/{1}-{2}/{1}-{2}.tgz".format(self.homepage, self.name, self.version),
                  sha256="04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmakeFile = os.path.join(self._source_folder, "build", "cmake")
        cmake = CMake(self)
        cmake.definitions["BUILD_UTILS"] = False
        cmake.configure(source_folder=cmakeFile, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absoluts paths. Let conan generate it.
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'pkgconfig'))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindSOIL.cmake.
        self.cpp_info.names["cmake_find_package"] = "GLEW"
        self.cpp_info.names["cmake_find_package_multi"] = "GLEW"

        # Set the name of conan auto generated glew.pc.
        self.cpp_info.names["pkg_config"] = "glew"

        # Set the package folder as CMAKE_PREFIX_PATH to find glew-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

        if self.settings.os == "Windows":

            if not self.options.shared:
                self.cpp_info.defines.append("GLEW_STATIC")

            if self.settings.compiler == "Visual Studio":
                if not self.options.shared:
                    self.cpp_info.libs.append("OpenGL32.lib")
                    if self.settings.compiler.runtime != "MT":
                        self.cpp_info.exelinkflags.append('-NODEFAULTLIB:LIBCMTD')
                        self.cpp_info.exelinkflags.append('-NODEFAULTLIB:LIBCMT')
            else:
                self.cpp_info.libs.append("opengl32")

        else:
            if self.settings.os == "Macos":
                self.cpp_info.exelinkflags.append("-framework OpenGL")
            elif not self.options.shared:
                self.cpp_info.libs.append("GL")
