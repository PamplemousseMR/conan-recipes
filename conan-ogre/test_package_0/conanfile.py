import os
from conans import ConanFile, CMake


class TestPackageConan(ConanFile):
    name = "test_package"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("plugins.cfg", dst="bin", src="bin")
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        bin_path = os.path.join("bin", self.name)
        self.run(bin_path, run_environment=True)
