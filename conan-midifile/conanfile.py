import os
from conans import ConanFile, tools, CMake

class MidifileConan(ConanFile):
    name = "midifile"
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
    exports_sources = [
        os.path.join("patches", "CMakeLists-0.1.txt.patch"),
        os.path.join("patches", "CMakeLists-0.2.txt.patch")
    ]
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        git = tools.Git(folder=self._source_folder)
        git.clone(**self.conan_data["sources"][self.version])
        os.rename("{0}_sources".format(self.name), self._source_folder)
        git.checkout(self.conan_data["commit"][self.version])

    def build(self):
        if self.conan_data["patches"][self.version]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(base_path=self._source_folder, patch_file=os.path.join("patches", patch), strip=0)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copy the license file.
        self.copy("LICENSE.txt", src=self._source_folder, dst="licenses", keep_path=False)

        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)