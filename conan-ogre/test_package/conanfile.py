import os
from conans import ConanFile, CMake


class TestPackageConan(ConanFile):
    name = "test_package"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        if self.settings.os == 'Windows':
            self.copy("plugins.cfg", dst="bin", src="bin")
        else:
            self.copy("plugins.cfg", dst="bin", src=os.path.join("share", "OGRE"))
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib", keep_path=False)

    def test(self):
        if self.settings.compiler == "Visual Studio":
            bin_path = os.path.join(str(self.settings.build_type), self.name)
        else:
            bin_path = self.name
        self.run(os.path.join(".", bin_path), run_environment=True)
