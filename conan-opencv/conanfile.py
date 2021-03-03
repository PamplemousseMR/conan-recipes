import os
from conans import ConanFile, tools, CMake


class OpenCVConan(ConanFile):
    name = "opencv"
    version = "4.5.1"
    description = "Open Source Computer Vision Library"
    homepage = "https://github.com/opencv/opencv"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Apache"
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
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="e27fe5b168918ab60d58d7ace2bd82dd14a4d0bd1d3ae182952c2113f5637513")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)
        #cmake.definitions["BUILD_UTILS"] = False
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE", src=self._source_folder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindOpenCV.cmake.
        self.cpp_info.names["cmake_find_package"] = "OpenCV"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenCV"

        # Set the name of conan auto generated opencv.pc.
        self.cpp_info.names["pkg_config"] = "OpenCV"

        # Set the package folder as CMAKE_PREFIX_PATH to find OpenCVConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
