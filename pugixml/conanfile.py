import os
import textwrap
from conans import ConanFile, tools, CMake

class PubixmlConan(ConanFile):
    name = "pugixml"
    description = "Light-weight, simple and fast XML parser for C++ with XPath support"
    homepage = "https://github.com/zeux/pugixml"
    url = "https://github.com/PamplemousseMR/conan-recipes"
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
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    @property
    def _module_subfolder(self):
        return os.path.join("lib", "cmake")

    @property
    def _module_file(self):
        return "conan-{}-targets.cmake".format(self.name) 

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
        if tools.Version(self.version) >= "1.10":
            self.copy("LICENSE.md", src=self._source_folder, dst="licenses", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        if tools.Version(self.version) >= "1.10":
            tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

        if self.options.header_only:
            source_dir = os.path.join(self._source_folder, "src")
            self.copy(pattern="*", dst="include", src=source_dir)
        else:
            self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        # Name of the find package file: FindFreetype.cmake
        self.cpp_info.filenames["cmake_find_package"] = "pugixml"
        self.cpp_info.filenames["cmake_find_package_multi"] = "pugixml"

        # name of the target: pugixml::pugixml
        self.cpp_info.name = "pugixml"
        self.cpp_info.names["pkg_config"] = "pugixml"

        if tools.Version(self.version) <= "1.10":
            # Create custom target: pugixml
            content = textwrap.dedent("""\
                    if(TARGET pugixml::pugixml AND NOT TARGET pugixml)
                        add_library(pugixml INTERFACE IMPORTED)
                        set_target_properties(pugixml PROPERTIES INTERFACE_LINK_LIBRARIES pugixml::pugixml)
                    endif()
                """)
            tools.save(os.path.join(self.package_folder, self._module_subfolder, self._module_file), content)

            self.cpp_info.builddirs.append(self._module_subfolder)
            module_rel_path = os.path.join(self._module_subfolder, self._module_file)
            self.cpp_info.build_modules["cmake_find_package"] = [module_rel_path]
            self.cpp_info.build_modules["cmake_find_package_multi"] = [module_rel_path]

        # Libraries
        if self.options.header_only:
            self.cpp_info.defines = ["PUGIXML_HEADER_ONLY"]
        else:
            self.cpp_info.libs = tools.collect_libs(self)

        # Set the package folder as CMAKE_PREFIX_PATH to find pugixml-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)