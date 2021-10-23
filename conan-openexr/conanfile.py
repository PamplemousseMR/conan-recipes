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
        # Name of the find package file: findOpenEXR.cmake
        self.cpp_info.filenames["cmake_find_package"] = "OpenEXR"
        self.cpp_info.filenames["cmake_find_package_multi"] = "OpenEXR"

        # Name of the target: OpenEXR::
        self.cpp_info.name = "OpenEXR"

        parsed_version = self.version.split(".")
        version_suffix = "-%s_%s" % (parsed_version[0], parsed_version[1])
        if not self.options.shared:
            version_suffix += "_s"
        if self.settings.compiler == "Visual Studio" and self.settings.build_type == "Debug":
            version_suffix += "_d"

        if tools.Version(self.version) <= "2.5.3":
            # Create the target: OpenEXR::IlmImfConfig
            self.cpp_info.components["IlmImfConfig"].name = "IlmImfConfig"
            self.cpp_info.components["IlmImfConfig"].includedirs.append(os.path.join(self.cpp_info.includedirs[0], "OpenEXR"))

            # Create the target: OpenEXR::IlmImf
            self.cpp_info.components["IlmImf"].name = "IlmImf"
            self.cpp_info.components["IlmImf"].libs = [ "IlmImf{}".format(version_suffix), 
                                                        "Iex{}".format(version_suffix),
                                                        "Half{}".format(version_suffix),
                                                        "Imath{}".format(version_suffix),
                                                        "IlmThread{}".format(version_suffix) ]
            self.cpp_info.components["IlmImf"].requires = ["IlmImfConfig", "zlib::zlib"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["IlmImf"].defines = ["OPENEXR_DLL"]
                
            # Create the target: OpenEXR::IlmImfConfig
            self.cpp_info.components["IlmImfUtil"].name = "IlmImfUtil"
            self.cpp_info.components["IlmImfUtil"].libs = [ "IlmImfUtil{}".format(version_suffix) ]
            self.cpp_info.components["IlmImfUtil"].requires = ["IlmImfConfig", "IlmImf"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["IlmImfUtil"].defines = ["OPENEXR_DLL"]

        elif tools.Version(self.version) <= "3.1.1":
            # Create the target: OpenEXR::OpenEXRConfig
            self.cpp_info.components["OpenEXRConfig"].name = "OpenEXRConfig"
            self.cpp_info.components["OpenEXRConfig"].includedirs.append(os.path.join(self.cpp_info.includedirs[0], "OpenEXR"))

            # Create the target: OpenEXR::IexConfig
            self.cpp_info.components["IexConfig"].name = "IexConfig"
            self.cpp_info.components["IexConfig"].includedirs.append(os.path.join(self.cpp_info.includedirs[0], "OpenEXR"))

            # Create the target: OpenEXR::IlmThreadConfig
            self.cpp_info.components["IlmThreadConfig"].name = "IlmThreadConfig"
            self.cpp_info.components["IlmThreadConfig"].includedirs.append(os.path.join(self.cpp_info.includedirs[0], "OpenEXR"))
        
            # Create the target: OpenEXR::Iex
            self.cpp_info.components["Iex"].name = "Iex"
            self.cpp_info.components["Iex"].libs = ["Iex{}".format(version_suffix)]
            self.cpp_info.components["Iex"].requires = ["IlmThreadConfig"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["Iex"].defines = ["OPENEXR_DLL"]

            # Create the target: OpenEXR::IlmThread
            self.cpp_info.components["IlmThread"].name = "IlmThread"
            self.cpp_info.components["IlmThread"].libs = ["IlmThread{}".format(version_suffix)]
            self.cpp_info.components["IlmThread"].requires = ["IlmThreadConfig", "Iex"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["IlmThread"].defines = ["OPENEXR_DLL"]
            if tools.os_info.is_linux:
                self.cpp_info.components["IlmThread"].system_libs.append("pthread")

            if tools.Version(self.version) > "3.0.5":
                # Create the target: OpenEXR::OpenEXRCore
                self.cpp_info.components["OpenEXRCore"].name = "OpenEXRCore"
                self.cpp_info.components["OpenEXRCore"].libs = ["OpenEXRCore{}".format(version_suffix)]
                self.cpp_info.components["OpenEXRCore"].requires = ["IlmThreadConfig", "zlib::zlib"]
                if self.options.shared and self.settings.os == "Windows":
                    self.cpp_info.components["OpenEXR"].defines = ["OPENEXR_DLL"]

            # Create the target: OpenEXR::OpenEXR
            self.cpp_info.components["OpenEXR"].name = "OpenEXR"
            self.cpp_info.components["OpenEXR"].libs = ["OpenEXR{}".format(version_suffix)]
            self.cpp_info.components["OpenEXR"].requires = ["IlmThreadConfig", "Iex", "IlmThread", "imath::imath", "zlib::zlib"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["OpenEXR"].defines = ["OPENEXR_DLL"]

            # Create the target: OpenEXR::OpenEXRUtil
            self.cpp_info.components["OpenEXRUtil"].name = "OpenEXRUtil"
            self.cpp_info.components["OpenEXRUtil"].libs = ["OpenEXRUtil{}".format(version_suffix)]
            self.cpp_info.components["OpenEXRUtil"].requires = ["IlmThreadConfig", "OpenEXR"]
            if self.options.shared and self.settings.os == "Windows":
                self.cpp_info.components["OpenEXRUtil"].defines = ["OPENEXR_DLL"]

        # Set the package folder as CMAKE_PREFIX_PATH to OpenEXRConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
