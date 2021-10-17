import os
from conans import ConanFile, tools, CMake

class OpenEXRConan(ConanFile):
    name = "openexr"
    description = "The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry"
    homepage = "https://github.com/AcademySoftwareFoundation/openexr"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }
    exports_sources = "CMakeLists.txt"
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def requirements(self):
        for requirement in self.conan_data["requirements"][self.version]:
            self.requires.add("{0}@{1}/{2}".format(requirement, self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def _patch_files(self):
        if tools.Version(self.version) <= "2.5.7":
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
        cmake.definitions["OPENEXR_BUILD_TOOLS"] = False
        cmake.definitions["OPENEXR_INSTALL_EXAMPLES"] = False
        cmake.definitions["OPENEXR_INSTALL_TOOLS"] = False
        cmake.definitions["OPENEXR_BUILD_BOTH_STATIC_SHARED"] = False
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE.md", src=self._source_folder, dst="licenses")
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        if tools.Version(self.version) <= "2.5.3":
            tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        self.cpp_info.includedirs.append(os.path.join(self.cpp_info.includedirs[0], "OpenEXR"))

        # Set the name of conan auto generated FindOpenEXR.cmake.
        self.cpp_info.name = "OpenEXR"

        # Set the package folder as CMAKE_PREFIX_PATH to find OpenEXRConfig.cmake and IlmBaseConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
