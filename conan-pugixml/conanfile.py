import os
from conans import ConanFile, tools, CMake


class PubixmlConan(ConanFile):
    name = "pugixml"
    description = "Light-weight, simple and fast XML parser for C++ with XPath support"
    homepage = "https://github.com/zeux/pugixml"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "MIT"
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
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

        if self.options.header_only:
            self.settings.clear()
            
    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def package_id(self):
        if self.options.header_only:
            self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
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
        # Copy the license file.
        self.copy("LICENSE.md", src=self._source_folder, dst="licenses", keep_path=False)

        # Remove the pkg config, it contains absoluts paths. Let conan generate it.
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'pkgconfig'))
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'cmake'))

        if self.options.header_only:
            source_dir = os.path.join(self._source_folder, "src")
            self.copy(pattern="*", dst="include", src=source_dir)
        else:
            self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Set the name of conan auto generated Findpugixml.cmake.
        self.cpp_info.names["cmake_find_package"] = "pugixml"
        self.cpp_info.names["cmake_find_package_multi"] = "pugixml"

        if self.options.header_only:
            self.cpp_info.defines = ["PUGIXML_HEADER_ONLY"]
        else:
            self.cpp_info.libs = tools.collect_libs(self)
