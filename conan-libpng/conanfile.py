from conans import ConanFile, tools, CMake
import os
import shutil

class LibpngConan(ConanFile):
    name = "libpng"
    version = "1.6.37"
    description = "LIBPNG: Portable Network Graphics support, official libpng repository http://libpng.sf.net"
    homepage = "https://github.com/glennrp/libpng"
    url = "https://github.com/PamplemousseMR/conan-libpng"
    license = "libpng-2.0"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
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
    exports = "LICENSE.md"
    exports_sources = os.path.join("patches", "CMakeLists.txt")
    short_paths=True
    
    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if tools.os_info.is_windows:
            self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256="ca74a0dace179a8422187671aee97dd3892b53e168627145271cad5b5ac81307")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)
        os.rename(os.path.join(self._source_folder, "CMakeLists.txt"), os.path.join(self._source_folder, "WrappedCMakeLists.txt"))
        shutil.copy(self.exports_sources, self._source_folder)

    def build(self):
        cmake = CMake(self)  
        cmake.definitions["LIBPNG_CONAN_INFO_DIR"] = self.build_folder
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
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)        
        for export in self.exports:
            self.copy(export, keep_path=False)
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'libpng'))
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'pkgconfig'))
        if tools.os_info.is_windows:
            os.remove(os.path.join(self.package_folder, 'bin', 'pngfix.exe'))
            os.remove(os.path.join(self.package_folder, 'bin', 'png-fix-itxt.exe'))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["cmake_find_package"] = "PNG"
        self.cpp_info.names["cmake_find_package_multi"] = "PNG"
        if not tools.os_info.is_windows:
            self.cpp_info.libs.extend(['z'])