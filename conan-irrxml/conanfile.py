import os
import shutil
from conans import ConanFile, tools, CMake


class IrrXMLConan(ConanFile):
    name = "irrxml"
    description = "Simple and fast open source xml parser for C++"
    homepage = "http://www.ambiera.com/irrxml"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "irrXML"
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
        os.path.join("patches", "CMakeLists.txt"),
        os.path.join("patches", "IrrXMLConfig.cmake.in"),
        os.path.join("patches", "irrTypes.h.patch")
    ]
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
        for export_source in self.conan_data["export_sources"][self.version]:
            shutil.copy(os.path.join("patches", export_source), self._source_folder)

    def build(self):
        if self.conan_data["patches"][self.version]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(base_path=self._source_folder, patch_file=os.path.join("patches", patch), strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindIrrXML.cmake.
        self.cpp_info.names["cmake_find_package"] = "IRRXML"
        self.cpp_info.names["cmake_find_package_multi"] = "IRRXML"

        # Set the name of conan auto generated IrrXML.pc.
        self.cpp_info.names["pkg_config"] = "IRRXML"

        # Set the package folder as CMAKE_PREFIX_PATH to find IrrXMLConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
