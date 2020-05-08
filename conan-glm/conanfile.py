from conans import ConanFile, tools
import os
from distutils.dir_util import copy_tree

class GlmConan(ConanFile):
    name = "glm"
    version = "0.9.9.7"
    description = "OpenGL Mathematics (GLM)"
    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/PamplemousseMR/conan-glm"
    license = "MIT"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    exports = "LICENSE.md"
    short_paths=True
    no_copy_source = True

    _source_folder = "{0}-{1}_sources".format(name, version)

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256="2ec9e33a80b548892af64fbd84a947f93f0e725423b1b7bec600f808057a8239")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def package(self):
        for export in self.exports:
            self.copy(export, keep_path=False)
        copy_tree(
            os.path.join(self.source_folder, self._source_folder, self.name),
            os.path.join(self.package_folder, "include", self.name))