from conans import ConanFile, tools, CMake
import os

class MidifileConan(ConanFile):
    name = "midifile"
    version = "1.0"
    description = "C++ classes for reading/writing Standard MIDI Files http://midifile.sapp.org"
    homepage = "https://github.com/craigsapp/midifile"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-2-Clause"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
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
    exports = "LICENSE.md"
    exports_sources = os.path.join("patches", "CMakeLists.txt.patch")
    short_paths=True
    
    _source_folder = "{0}-{1}_sources".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        
    def source(self):
        tools.get("{0}/archive/master.tar.gz".format(self.homepage), sha256="5d51d9e7ad5648a14287d391e0fba5c254898565a934a0b2b9720b34773a81be")
        os.rename("{0}-master".format(self.name), self._source_folder)

    def build(self):
        tools.patch(base_path=self._source_folder, patch_file=self.exports_sources, strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)        
        for export in self.exports:
            self.copy(export, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)