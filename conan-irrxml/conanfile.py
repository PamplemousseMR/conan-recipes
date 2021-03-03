import os
import shutil
from conans import ConanFile, tools, CMake


class IrrXMLConan(ConanFile):
    name = "irrxml"
    version = "1.2"
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

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def source(self):
        tools.get("http://prdownloads.sourceforge.net/irrlicht/irrxml-{0}.zip".format(self.version),
                  sha256="9b4f80639b2dee3caddbf75862389de684747df27bea7d25f96c7330606d7079")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
        shutil.copy(self.exports_sources[0], self._source_folder)
        shutil.copy(self.exports_sources[1], self._source_folder)

    def build(self):
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources[2], strip=0)
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
