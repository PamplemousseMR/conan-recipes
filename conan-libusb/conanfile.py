from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild
import os
import shutil

class LibUSBConan(ConanFile):
    name = "libusb"
    version = "1.0.23"
    description = "A cross-platform library to access USB devices"
    homepage = "https://github.com/libusb/libusb"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "LGPL-2.1"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_udev": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "enable_udev": True
    }
    short_paths=True
    
    _source_folder = "{0}-{1}_sources".format(name, version)

    @property
    def _is_mingw(self):
        return self.settings.os == "Windows" and self.settings.compiler == "gcc"

    @property
    def _is_msvc(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def config_options(self):
        if self.settings.os != "Linux":
            del self.options.enable_udev
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get("{0}/releases/download/v{1}/libusb-{1}.tar.bz2".format(self.homepage, self.version), sha256="db11c06e958a82dac52cf3c65cb4dd2c3f339c8a988665110e0d24d19312ad8d")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def _build_visual_studio(self):
        with tools.chdir(self._source_folder):
            # Find the sln file.
            solution_file = "libusb_2017.sln"
            if self.settings.compiler.version == "16":
                solution_file = "libusb_2017.sln"
            if self.settings.compiler.version == "15":
                solution_file = "libusb_2017.sln"
            if self.settings.compiler.version == "14":
                solution_file = "libusb_2015.sln"
            if self.settings.compiler.version == "12":
                solution_file = "libusb_2013.sln"
            elif self.settings.compiler.version == "11":
                solution_file = "libusb_2012.sln"
            solution_file = os.path.join("msvc", solution_file)
            platforms = {"x86":"Win32"}
            # Generate the sln project.
            msbuild = MSBuild(self)
            msbuild.build(solution_file, platforms=platforms, upgrade_project=False)

    def _build_autotools(self):
        # Use autotools to build the library.
        autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        configure_args = ["--enable-shared" if self.options.shared else "--disable-shared"]
        configure_args.append("--enable-static" if not self.options.shared else "--disable-static")
        if self.settings.os == "Linux":
            configure_args.append("--enable-udev" if self.options.enable_udev else "--disable-udev")
        elif self._is_mingw :
            if self.settings.arch == "x86_64":
                configure_args.append("--host=x86_64-w64-mingw32")
            elif self.settings.arch == "x86":
                configure_args.append("--build=i686-w64-mingw32")
                configure_args.append("--host=i686-w64-mingw32")
        autotools.configure(args=configure_args, configure_dir=self._source_folder)
        autotools.make()
        autotools.install()

    def build(self):
        if self._is_msvc :
            # Patch all vcxproj.
            for vcxproj in ["fxload_2017", "getopt_2017", "hotplugtest_2017", "libusb_dll_2017", "libusb_static_2017", "listdevs_2017", "stress_2017", "testlibusb_2017", "xusb_2017"]:
                vcxproj_path = os.path.join(self._source_folder, "msvc", "%s.vcxproj" % vcxproj)
                tools.replace_in_file(vcxproj_path, "<WindowsTargetPlatformVersion>10.0.16299.0</WindowsTargetPlatformVersion>", "")
            self._build_visual_studio()
        else:
            self._build_autotools()

    def package(self):
        # Copying the license file.
        self.copy("COPYING", src=self._source_folder, dst="licenses", keep_path=False)
        if self._is_msvc :
            # Package header, lib, dll and pdb.
            self.copy(pattern="libusb.h", dst=os.path.join("include", "libusb-1.0"), src=os.path.join(self._source_folder, "libusb"), keep_path=False)
            arch = "x64" if self.settings.arch == "x86_64" else "Win32"
            source_dir = os.path.join(self._source_folder, arch, str(self.settings.build_type), "dll" if self.options.shared else "lib")
            self.copy(pattern="*.pdb", dst="bin", src=source_dir, keep_path=False)
            self.copy(pattern="libusb-usbdk-1.0.dll", dst="bin", src=source_dir, keep_path=False)
            self.copy(pattern="libusb-usbdk-1.0.lib", dst="lib", src=source_dir, keep_path=False)
            if self.options.shared:
                self.copy(pattern="libusb-1.0.dll", dst="bin", src=source_dir, keep_path=False)
                self.copy(pattern="libusb-1.0.lib", dst="lib", src=source_dir, keep_path=False)
        else:
            # Remove the pkg config, it contains absoluts paths. Let conan generate it.
            tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
            # Remove the file generate by libtool.
            la_file = os.path.join(self.package_folder, "lib", "libusb-1.0.la")
            if os.path.isfile(la_file):
                os.remove(la_file)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        # Set the name of conan auto generated FindLibUSB.cmake.
        self.cpp_info.names["cmake_find_package"] = "LibUSB"
        self.cpp_info.names["cmake_find_package_multi"] = "LibUSB"
        # Set the name of conan auto generated libusb-1.0.pc.
        self.cpp_info.names["pkg_config"] = "libusb-1.0"
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
            if self.options.enable_udev:
                self.cpp_info.system_libs.append("udev")
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["IOKit", "CoreFoundation"])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs = ["advapi32"]