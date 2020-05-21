from conans import ConanFile, CMake, tools
import os

class TestPackageConan(ConanFile):
    name = "test_package"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def configure(self):
        del self.settings.compiler.libcxx

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", self.name)
        self.run(bin_path, run_environment=True)