import os
from conans import ConanFile, tools, CMake


class MidifileConan(ConanFile):
    name = "midifile"
    version = "1.0"
    description = "C++ classes for reading/writing Standard MIDI Files http://midifile.sapp.org"
    homepage = "https://github.com/craigsapp/midifile"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-2-Clause"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
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

    def source(self):
        tools.get("{0}/archive/master.tar.gz".format(self.homepage),
                  sha256="6dce0f303c4da6ae6df2ab5424d287ffb3e77a40d19c7ce6665513f83ad42a9c")
        os.rename("{0}-master".format(self.name), self._source_folder)

    def build(self):
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources, strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
