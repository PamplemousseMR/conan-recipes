import os
from conans import ConanFile, CMake

class TestPackageConan(ConanFile):
    name = "test_package"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if self.settings.compiler == "Visual Studio":
            bin_path = os.path.join(str(self.settings.build_type), self.name)
        else:
            bin_path = self.name
        self.run(os.path.join(".", bin_path) + " --help", run_environment=True)
