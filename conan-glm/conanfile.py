import os
from conans import ConanFile, tools
from distutils.dir_util import copy_tree


class GlmConan(ConanFile):
    name = "glm"
    version = "0.9.9.8"
    description = "OpenGL Mathematics (GLM)"
    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "MIT"
    short_paths = True
    no_copy_source = True

    _source_folder = "{0}-{1}_sources".format(name, version)

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="7d508ab72cb5d43227a3711420f06ff99b0a0cb63ee2f93631b162bfe1fe9592")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def package(self):
        # Copying the license file.
        self.copy("copying.txt", src=self._source_folder, dst="licenses", keep_path=False)
        copy_tree(
            os.path.join(self.source_folder, self._source_folder, "glm"),
            os.path.join(self.package_folder, "include", "glm"))
        os.remove(os.path.join(self.package_folder, "include", "glm", "CMakeLists.txt"))

    def package_info(self):
        # Set the name of conan auto generated FindGLM.cmake.
        self.cpp_info.names["cmake_find_package"] = "GLM"
        self.cpp_info.names["cmake_find_package_multi"] = "GLM"
