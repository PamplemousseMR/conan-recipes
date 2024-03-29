import os
import textwrap
from conans import ConanFile, tools, CMake

class FreetypeConan(ConanFile):
    name = "freetype"
    description = "FreeType is a freely available software library to render fonts"
    homepage = "https://download.savannah.gnu.org/releases/freetype/"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_zlib": [True, False],
        "with_bzip2": [True, False],
        "with_png": [True, False],
        "with_harfbuzz": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_zlib": True,
        "with_bzip2": True,
        "with_png": True,
        "with_harfbuzz": False
    }
    exports_sources = "CMakeLists.txt"
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

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/{0}@{1}/{2}".format(self.conan_data["bzip2"][self.version], self.user, self.channel))

        if self.options.with_harfbuzz:
            self.requires.add("harfbuzz/{0}@{1}/{2}".format(self.conan_data["harfbuzz"][self.version], self.user, self.channel))

        if self.options.with_png:
            if not self.options.with_zlib:
                self.output.warn("libpng needs zlib, with_png is sets to False.")
                self.options.with_png = False
            else:
                self.requires.add("libpng/{0}@{1}/{2}".format(self.conan_data["libpng"][self.version], self.user, self.channel))

        if self.options.with_zlib:
            self.requires.add("zlib/{0}@{1}/{2}".format(self.conan_data["zlib"][self.version], self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-VER-{1}-{2}-{3}".format(self.name, self.version.as_list[0], self.version.as_list[1], self.version.as_list[2]), self._source_folder)

    def build(self):
        cmake = CMake(self)

        cmake.definitions["FT_WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_ZLIB"] = not self.options.with_zlib

        cmake.definitions["FT_WITH_BZIP2"] = self.options.with_bzip2
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_BZip2"] = not self.options.with_bzip2

        cmake.definitions["FT_WITH_PNG"] = self.options.with_png
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_PNG"] = not self.options.with_png

        cmake.definitions["FT_WITH_HARFBUZZ"] = self.options.with_harfbuzz
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_HarfBuzz"] = not self.options.with_harfbuzz

        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy(os.path.join("docs", "LICENSE.TXT"), src=self._source_folder, dst="licenses", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)
        
        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # Name of the find package file: FindFreetype.cmake
        self.cpp_info.filenames["cmake_find_package"] = "Freetype"
        self.cpp_info.filenames["cmake_find_package_multi"] = "Freetype"

        # name of the target: Freetype::Freetype
        self.cpp_info.name = "Freetype"
        self.cpp_info.names["pkg_config"] = "freetype2"

        # Create custom target: freetype
        content = textwrap.dedent("""\
                if(TARGET Freetype::Freetype AND NOT TARGET freetype)
                    add_library(freetype INTERFACE IMPORTED)
                    set_target_properties(freetype PROPERTIES INTERFACE_LINK_LIBRARIES Freetype::Freetype)
                endif()
            """)
        tools.save(os.path.join(self.package_folder, self._module_subfolder, self._module_file), content)

        self.cpp_info.builddirs.append(self._module_subfolder)
        module_rel_path = os.path.join(self._module_subfolder, self._module_file)
        self.cpp_info.build_modules["cmake_find_package"] = [module_rel_path]
        self.cpp_info.build_modules["cmake_find_package_multi"] = [module_rel_path]

        # Libraries
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join(self.cpp_info.includedirs[0], "freetype2"))

        # Set the package folder as CMAKE_PREFIX_PATH to find freetype-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
