import os
from conans import ConanFile, tools, CMake

class ImathConan(ConanFile):
    name = "imath"
    description = "Imath is a C++ and python library of 2D and 3D vector, matrix, and math operations for computer graphics"
    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
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

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("Imath-{0}".format(self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PYTHON"] = False
        cmake.definitions["DOCS"] = False
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE.md", src=self._source_folder, dst="licenses")
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Name of the find package file: FindImath.cmake
        self.cpp_info.filenames["cmake_find_package"] = "Imath"
        self.cpp_info.filenames["cmake_find_package_multi"] = "Imath"

        # name of the target: Imath::
        self.cpp_info.name = "Imath"

        # Create the target: OpenEXR::ImathConfig
        self.cpp_info.components["ImathConfig"].name = "ImathConfig"
        self.cpp_info.components["ImathConfig"].includedirs.append(os.path.join(self.cpp_info.includedirs[0], "Imath"))

        # Create the target: OpenEXR::Imath
        self.cpp_info.components["target"].name = "Imath"
        self.cpp_info.components["target"].libs = tools.collect_libs(self)
        self.cpp_info.components["target"].requires = ["ImathConfig"]
        if self.options.shared and tools.os_info.is_windows:
            self.cpp_info.components["target"].defines = ["IMATH_DLL"]

        # Set the package folder as CMAKE_PREFIX_PATH to find ImathConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
