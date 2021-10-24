import os
from conans import ConanFile, tools
from distutils.dir_util import copy_tree

class GlmConan(ConanFile):
    name = "glm"
    description = "OpenGL Mathematics (GLM)"
    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "MIT"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    short_paths = True
    no_copy_source = True

    _source_folder = "{0}_sources".format(name)

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def package(self):
        # Copying the license file.
        self.copy("copying.txt", src=self._source_folder, dst="licenses", keep_path=False)
        copy_tree(
            os.path.join(self.source_folder, self._source_folder, "glm"),
            os.path.join(self.package_folder, "include", "glm"))
        os.remove(os.path.join(self.package_folder, "include", "glm", "CMakeLists.txt"))

    def package_info(self):
        # Name of the find package file: FindGLM.cmake
        self.cpp_info.filenames["cmake_find_package"] = "GLM"
        self.cpp_info.filenames["cmake_find_package_multi"] = "GLM"

        # name of the target: GLM::GLM
        self.cpp_info.name = "GLM"