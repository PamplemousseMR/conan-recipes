import os
from conans import ConanFile, tools, CMake


class LibpngConan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "LIBPNG: Portable Network Graphics support, official libpng repository http://libpng.sf.net"
    homepage = "https://github.com/glennrp/libpng"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "libpng-2.0"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "hardware_optimizations": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "hardware_optimizations": True
    }
    exports_sources = os.path.join("patches", "CMakeLists.txt.patch")
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
        self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version),
                  sha256="ca74a0dace179a8422187671aee97dd3892b53e168627145271cad5b5ac81307")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources, strip=0)
        cmake = CMake(self)
        cmake.definitions["PNG_BUILD_ZLIB"] = False
        cmake.definitions["PNG_DEBUG"] = False if self.settings.build_type == "Release" else True
        cmake.definitions["PNG_FRAMEWORK"] = False
        cmake.definitions["PNG_HARDWARE_OPTIMIZATIONS"] = self.options.hardware_optimizations
        cmake.definitions["PNG_SHARED"] = self.options.shared
        cmake.definitions["PNG_STATIC"] = not self.options.shared
        cmake.definitions["PNG_TESTS"] = False
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", src=self._source_folder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove executables.
        if tools.os_info.is_windows:
            os.remove(os.path.join(self.package_folder, 'bin', 'pngfix.exe'))
            os.remove(os.path.join(self.package_folder, 'bin', 'png-fix-itxt.exe'))

        tools.rmdir(os.path.join(self.package_folder, 'share'))
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'libpng'))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindPNG.cmake.
        self.cpp_info.names["cmake_find_package"] = "PNG"
        self.cpp_info.names["cmake_find_package_multi"] = "PNG"