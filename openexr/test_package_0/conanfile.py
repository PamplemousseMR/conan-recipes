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

    def test(self):
        bin_path = os.path.join("bin", self.name)
        self.run("{0} comp_short_decode_piz.exr".format(bin_path), run_environment=True)
