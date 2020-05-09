from conans import ConanFile, tools, CMake
import os

class PubixmlConan(ConanFile):
    name = "pugixml"
    version = "1.10"
    description = "Light-weight, simple and fast XML parser for C++ with XPath support"
    homepage = "https://github.com/zeux/pugixml"
    url = "https://github.com/PamplemousseMR/conan-pugixml"
    license = "MIT"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "header_only": [True, False],
        "wchar_mode": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "header_only": False,
        "wchar_mode": False
    }
    exports = "LICENSE.md"
    short_paths=True

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        del self.settings.compiler.libcxx

        if tools.os_info.is_windows:
            del self.options.fPIC

        if self.options.header_only:
            self.settings.clear()

    def package_id(self):
        if self.options.header_only:
            self.info.header_only()

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256="10f1f0a32b559ca8435d95855928d990cfbb9796e339efb638080c897728174c")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        header_file = os.path.join(self._source_folder, "src", "pugiconfig.hpp")
        
        if self.options.wchar_mode:
            tools.replace_in_file(header_file, "// #define PUGIXML_WCHAR_MODE", '''#define PUGIXML_WCHAR_MODE''')
        
        if self.options.header_only:
            tools.replace_in_file(header_file, "// #define PUGIXML_HEADER_ONLY", '''#define PUGIXML_HEADER_ONLY''')
        else:
            cmake = CMake(self)            
            cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
            cmake.build()
            cmake.install()

    def package(self):
        if self.options.header_only:
            source_dir = os.path.join(self._source_folder, "src")
            self.copy(pattern="*", dst="include", src=source_dir)
        else:
            self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        for export in self.exports:
            self.copy(export, keep_path=False)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "PugiXML"
        self.cpp_info.names["cmake_find_package_multi"] = "PugiXML"
        if self.options.header_only:
            self.cpp_info.defines = ["PUGIXML_HEADER_ONLY"]
        else:
            self.cpp_info.libs = tools.collect_libs(self)