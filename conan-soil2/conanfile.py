import os
import shutil
from conans import ConanFile, tools, CMake


class Soil2Conan(ConanFile):
    name = "soil2"
    description = "Simple OpenGL Image Library"
    homepage = "https://github.com/SpartanJ/SOIL2"
    url = "https://github.com/PamplemousseMR/conan-recipes"
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
    exports_sources = [
        os.path.join("patches", "CMakeLists-1.07.txt"),
        os.path.join("patches", "CMakeLists-1.08.txt"),
        os.path.join("patches", "CMakeLists-1.09.txt"),
        os.path.join("patches", "CMakeLists-1.10.txt"),
        os.path.join("patches", "CMakeLists-1.11.txt"),
        os.path.join("patches", "CMakeLists-1.20.txt"),
        os.path.join("patches", "SOIL2Config.cmake.in")
    ]
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
        os.rename("SOIL2-release-{0}".format(self.version), self._source_folder)
        for export_source in self.conan_data["export_sources"][self.version]:
            shutil.copy(os.path.join("patches", export_source["file"]), self._source_folder)
            os.rename(os.path.join(self._source_folder, export_source["file"]),
                      os.path.join(self._source_folder, export_source["name"]))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copy the license file.
        if tools.Version(self.version) >= "1.20":
            self.copy("LICENSE", src=self._source_folder, dst="licenses", keep_path=False)

        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Set the name of conan auto generated FindSOIL2.cmake.
        self.cpp_info.name = "SOIL2"

        self.cpp_info.libs = tools.collect_libs(self)

        # Set the package folder as CMAKE_PREFIX_PATH to find SOIL2Config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

        if self.settings.os == "Linux":
            self.cpp_info.libs.append('GL')
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["OpenGL", "CoreFoundation"])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append('opengl32')
