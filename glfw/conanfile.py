import os
import textwrap
from conans import ConanFile, tools, CMake

class GlfwConan(ConanFile):
    name = "glfw"
    description = "A multi-platform library for OpenGL, OpenGL ES, Vulkan, window and input https://www.glfw.org/"
    homepage = "https://github.com/glfw/glfw"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Zlib"
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
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    @property
    def _module_subfolder(self):
        return os.path.join("lib", "cmake")

    @property
    def _module_file(self):
        return "conan-{}-targets.cmake".format(self.name)   
    
    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE.md", src=self._source_folder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # Name of the find package file: FindFreetype.cmake
        self.cpp_info.filenames["cmake_find_package"] = "glfw3"
        self.cpp_info.filenames["cmake_find_package_multi"] = "glfw3"

        # name of the target: glfw3::glfw3
        self.cpp_info.name = "glfw3"
        self.cpp_info.names["pkg_config"] = "glfw3"

        # Create custom target: glfw
        content = textwrap.dedent("""\
                if(TARGET glfw3::glfw3 AND NOT TARGET glfw)
                    add_library(glfw INTERFACE IMPORTED)
                    set_target_properties(glfw PROPERTIES INTERFACE_LINK_LIBRARIES glfw3::glfw3)
                endif()
            """)
        tools.save(os.path.join(self.package_folder, self._module_subfolder, self._module_file), content)

        self.cpp_info.builddirs.append(self._module_subfolder)
        module_rel_path = os.path.join(self._module_subfolder, self._module_file)
        self.cpp_info.build_modules["cmake_find_package"] = [module_rel_path]
        self.cpp_info.build_modules["cmake_find_package_multi"] = [module_rel_path]

        # Libraries
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the package folder as CMAKE_PREFIX_PATH to find glfw-config.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

        if tools.os_info.is_linux:
            self.cpp_info.system_libs.extend(["Xi", "dl", "X11", "pthread"])
        elif tools.os_info.is_macos:
            self.cpp_info.frameworks.extend(["Cocoa", "IOKit", "CoreVideo"])
