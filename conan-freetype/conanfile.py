import os
from conans import ConanFile, tools, CMake


class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.10.4"
    description = "FreeType is a freely available software library to render fonts"
    homepage = "https://download.savannah.gnu.org/releases/freetype/"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD"
    generators = "cmake_find_package"
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
        "with_zlib": False,
        "with_bzip2": False,
        "with_png": False,
        "with_harfbuzz": False
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

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.8@{0}/{1}".format(self.user, self.channel))

        if self.options.with_harfbuzz:
            self.requires.add("harfbuzz/2.6.2@{0}/{1}".format(self.user, self.channel))

        if self.options.with_png:
            self.requires.add("libpng/1.6.37@{0}/{1}".format(self.user, self.channel))
            if not self.options.with_zlib:
                self.output.warn("libpng needs zlib, with_png is sets to True.")
                self.options.with_zlib = True

        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/{1}-{2}.tar.gz".format(self.homepage, self.name, self.version),
                  sha256="5eab795ebb23ac77001cfb68b7d4d50b5d6c7469247b0b01b2c953269f658dac")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

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

        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy(os.path.join("docs", "LICENSE.TXT"), src=self._source_folder, dst="licenses", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join(self.cpp_info.includedirs[0], "freetype2"))

        # Set the name of conan auto generated FindFreetype.cmake.
        self.cpp_info.names["cmake_find_package"] = "Freetype"
        self.cpp_info.names["cmake_find_package_multi"] = "Freetype"

        # Set the package folder as CMAKE_PREFIX_PATH to find freetype-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
