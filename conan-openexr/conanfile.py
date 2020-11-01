import os
from conans import ConanFile, tools, CMake


class OpenEXRConan(ConanFile):
    name = "openexr"
    version = "2.5.3"
    description = "The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry"
    homepage = "https://github.com/AcademySoftwareFoundation/openexr"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
    generators = "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    short_paths = True

    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        self.requires.add("zlib/1.2.11@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version),
                  sha256="6a6525e6e3907715c6a55887716d7e42d09b54d2457323fcee35a0376960bebf")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def _patch_files(self):
        for lib in ("OpenEXR", "IlmBase"):
            if self.settings.build_type == "Debug":
                tools.replace_in_file(os.path.join(self._source_folder, lib, "config", "LibraryDefine.cmake"),
                                      "set(verlibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${@LIB@_LIB_SUFFIX}${CMAKE_SHARED_LIBRARY_SUFFIX})".replace(
                                          "@LIB@", lib.upper()),
                                      "set(verlibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${@LIB@_LIB_SUFFIX}_d${CMAKE_SHARED_LIBRARY_SUFFIX})".replace(
                                          "@LIB@", lib.upper()))
                tools.replace_in_file(os.path.join(self._source_folder, lib, "config", "LibraryDefine.cmake"),
                                      "set(baselibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${CMAKE_SHARED_LIBRARY_SUFFIX})",
                                      "set(baselibname ${CMAKE_SHARED_LIBRARY_PREFIX}${libname}_d${CMAKE_SHARED_LIBRARY_SUFFIX})")

    def build(self):
        self._patch_files()
        generator = None
        if self.settings.os == "Windows":
            generator = "NMake Makefiles"  # The default generator 'Visual Studio', doesn't works for the install target.
        cmake = CMake(self, generator=generator)
        cmake.definitions["OPENEXR_CONAN_INFO_DIR"] = self.build_folder
        cmake.definitions["PYILMBASE_ENABLE"] = False
        cmake.definitions["OPENEXR_VIEWERS_ENABLE"] = False
        cmake.definitions["OPENEXR_BUILD_BOTH_STATIC_SHARED"] = False
        cmake.definitions["OPENEXR_BUILD_UTILS"] = False
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE.md", src=self._source_folder, dst="licenses")
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absoluts paths. Let conan generate it.
        tools.rmdir(os.path.join(self.package_folder, 'lib', 'pkgconfig'))
        tools.rmdir(os.path.join(self.package_folder, 'share'))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        self.cpp_info.includedirs = [os.path.join("include", "OpenEXR"), "include"]

        # Set the name of conan auto generated FindOpenEXR.cmake.
        self.cpp_info.names["cmake_find_package"] = "OpenEXR"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenEXR"

        # Set the name of conan auto generated OpenEXR.pc.
        self.cpp_info.names["pkg_config"] = "OpenEXR"

        # Set the package folder as CMAKE_PREFIX_PATH to find OpenEXRConfig.cmake and IlmBaseConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
