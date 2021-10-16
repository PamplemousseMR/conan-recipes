import os
import shutil
from conans import ConanFile, tools, CMake

class OgreConan(ConanFile):
    name = "ogre"
    description = "Ogre1 - scene-oriented, flexible 3D engine written in C++ https://ogrecave.github.io/ogre/"
    homepage = "https://github.com/OGRECave/ogre"
    url = "https://github.com/PamplemousseMR/conan-ogre"
    license = "MIT"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "config_enable_gl_state_cache_support": [True, False],
        "config_double": [True, False],
        "config_enable_quad_buffer_stereo": [True, False],
        "config_enable_viewport_orientationmode": [True, False],
        "config_filesystem_unicode": [True, False],
        "config_node_inherit_transform": [True, False],
        "config_enable_astc": [True, False],
        "config_enable_dds": [True, False],
        "config_enable_etc": [True, False],
        "config_enable_pvrtc": [True, False],
        "config_enable_meshlod": [True, False],
        "config_enable_tbb_scheduler": [True, False],
        "config_enable_zzip": [True, False],
        "config_enable_gles2_cg_support": [True, False],
        "config_enable_gles2_glsl_optimiser": [True, False],
        "component_bites": [True, False],
        "component_paging": [True, False],
        "component_meshlodgenerator": [True, False],
        "component_property": [True, False],
        "component_terrain": [True, False],
        "component_rtshadersystem": [True, False],
        "rtshadersystem_shaders": [True, False],
        "component_volume": [True, False],
        "component_overlay": [True, False],
        "component_overlay_imgui": [True, False],
        "plugin_octree": [True, False],
        "plugin_bsp": [True, False],
        "plugin_cg": [True, False],
        "plugin_exrcodec": [True, False],
        "plugin_stbi": [True, False],
        "plugin_freeimage": [True, False],
        "plugin_pfx": [True, False],
        "plugin_pcz": [True, False],
        "plugin_dot_scene": [True, False],
        "plugin_assimp": [True, False],
        "rendersystem_d3d9": [True, False],
        "rendersystem_d3d11": [True, False],
        "rendersystem_gl": [True, False],
        "rendersystem_gl3plus": [True, False],
        "rendersystem_gles2": [True, False],
        "rendersystem_metal": [True, False],
        "rendersystem_tiny": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "config_enable_gl_state_cache_support": False,
        "config_double": False,
        "config_enable_quad_buffer_stereo": False, # TODO need NVAPI and AMDQBS
        "config_enable_viewport_orientationmode": False,
        "config_filesystem_unicode": True,
        "config_node_inherit_transform": False,
        "config_enable_astc": True,
        "config_enable_dds": True,
        "config_enable_etc": True,
        "config_enable_pvrtc": True,
        "config_enable_meshlod": True,
        "config_enable_tbb_scheduler": True,
        "config_enable_zzip": True,
        "config_enable_gles2_cg_support": False,
        "config_enable_gles2_glsl_optimiser": False,
        "component_bites": True,               
        "component_paging": True,
        "component_meshlodgenerator": True,
        "component_property": True,
        "component_terrain": True,
        "component_rtshadersystem": True,
        "rtshadersystem_shaders": True,
        "component_volume": True,
        "component_overlay": True,
        "component_overlay_imgui": True,
        "plugin_octree": True,
        "plugin_bsp": True,
        "plugin_cg": False, # Todo CG
        "plugin_exrcodec": False, # TODO openexr
        "plugin_stbi": False, # TODO error in the test
        "plugin_freeimage": False, # TODO Freeimage
        "plugin_pfx": True,
        "plugin_pcz": True,
        "plugin_dot_scene": True,
        "plugin_assimp": False, # TODO Assimp
        "rendersystem_d3d9": False,
        "rendersystem_d3d11": True,
        "rendersystem_gl": True,
        "rendersystem_gl3plus": True,
        "rendersystem_gles2": False,
        'rendersystem_metal': False,
        "rendersystem_tiny": True
    }
    exports_sources = "CMakeLists.txt"
    short_paths = False # TODO set to true

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    def config_options(self):
        super(OgreConan, self).config_options()

        if self.settings.os != 'Windows':
            del self.options.rendersystem_d3d11
            del self.options.rendersystem_d3d9

        if self.settings.os != 'Macos':
            del self.options.rendersystem_metal

    def configure(self):
        if self.options.component_bites and not self.options.component_overlay:
            self.output.warn("OgreBites component needs Overlay component to be built. The option is disable")
            self.options.component_bites = False

        if self.options.component_overlay_imgui and not self.options.component_overlay:
            self.output.warn("OgreBites component overlay needs Overlay component to be built. The option is disable")
            self.options.component_overlay_imgui = False

        if self.options.rtshadersystem_shaders and not self.options.component_rtshadersystem:
            self.output.warn("RT Shader System shaders component needs RTShader System component to be built. The option is disable")
            self.options.rtshadersystem_shaders = False

        if self.options.config_enable_gles2_cg_support and not self.options.rendersystem_gles2:
            self.output.warn("GLES CG suport config needs GLES Render System. The option is disable")
            self.options.config_enable_gles2_cg_support = False

        if self.options.config_enable_gles2_glsl_optimiser and not self.options.rendersystem_gles2:
            self.output.warn("GLES CG optimiser config needs GLES Render System. The option is disable")
            self.options.config_enable_gles2_glsl_optimiser = False

    def requirements(self):
        if self.options.component_overlay:
            self.requires("freetype/{0}@{1}/{2}".format(self.conan_data["freetype"][self.version], self.user, self.channel))
        if self.options.plugin_dot_scene:
            self.requires("pugixml/{0}@{1}/{2}".format(self.conan_data["pugixml"][self.version], self.user, self.channel))
        if self.options.plugin_exrcodec:
            self.requires("openexr/{0}@{1}/{2}".format(self.conan_data["openexr"][self.version], self.user, self.channel))
        if self.options.plugin_assimp:
            self.requires("assimp/{0}@{1}/{2}".format(self.conan_data["assimp"][self.version], self.user, self.channel))            

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)

        cmake.definitions['OGRE_ASSERT_MODE'] = 1
        cmake.definitions['OGRE_RESOURCEMANAGER_STRICT'] = '0'
        cmake.definitions['OGRE_STATIC'] = not self.options.shared

        cmake.definitions['OGRE_CONFIG_THREAD_PROVIDER'] = 'std'
        cmake.definitions['OGRE_CONFIG_THREAD'] = 3
        cmake.definitions['OGRE_CONFIG_ENABLE_GL_STATE_CACHE_SUPPORT'] = self.options.config_enable_gl_state_cache_support
        cmake.definitions['OGRE_CONFIG_DOUBLE'] = self.options.config_double
        cmake.definitions['OGRE_CONFIG_ENABLE_QUAD_BUFFER_STEREO'] = self.options.config_enable_quad_buffer_stereo
        cmake.definitions['OGRE_CONFIG_ENABLE_VIEWPORT_ORIENTATIONMODE'] = self.options.config_enable_viewport_orientationmode
        cmake.definitions['OGRE_CONFIG_FILESYSTEM_UNICODE'] = self.options.config_filesystem_unicode
        cmake.definitions['OGRE_CONFIG_NODE_INHERIT_TRANSFORM'] = self.options.config_node_inherit_transform
        cmake.definitions['OGRE_CONFIG_ENABLE_ASTC'] = self.options.config_enable_astc
        cmake.definitions['OGRE_CONFIG_ENABLE_DDS'] = self.options.config_enable_dds
        cmake.definitions['OGRE_CONFIG_ENABLE_ETC'] = self.options.config_enable_etc
        cmake.definitions['OGRE_CONFIG_ENABLE_PVRTC'] = self.options.config_enable_pvrtc
        cmake.definitions['OGRE_CONFIG_ENABLE_MESHLOD'] = self.options.config_enable_meshlod
        cmake.definitions['OGRE_CONFIG_ENABLE_TBB_SCHEDULER'] = self.options.config_enable_tbb_scheduler
        cmake.definitions['OGRE_CONFIG_ENABLE_ZIP'] = self.options.config_enable_zzip
        cmake.definitions['OGRE_CONFIG_ENABLE_GLES2_CG_SUPPORT'] = self.options.config_enable_gles2_cg_support
        cmake.definitions['OGRE_CONFIG_ENABLE_GLES2_GLSL_OPTIMISER'] = self.options.config_enable_gles2_glsl_optimiser

        cmake.definitions['OGRE_BUILD_COMPONENT_BITES'] = self.options.component_bites
        cmake.definitions['OGRE_BUILD_COMPONENT_PAGING'] = self.options.component_paging
        cmake.definitions['OGRE_BUILD_COMPONENT_MESHLODGENERATOR'] = self.options.component_meshlodgenerator
        cmake.definitions['OGRE_BUILD_COMPONENT_PROPERTY'] = self.options.component_property
        cmake.definitions['OGRE_BUILD_COMPONENT_TERRAIN'] = self.options.component_terrain
        cmake.definitions['OGRE_BUILD_COMPONENT_RTSHADERSYSTEM'] = self.options.component_rtshadersystem
        cmake.definitions['OGRE_BUILD_RTSHADERSYSTEM_SHADERS'] = self.options.rtshadersystem_shaders
        cmake.definitions['OGRE_BUILD_COMPONENT_VOLUME'] = self.options.component_volume
        cmake.definitions['OGRE_BUILD_COMPONENT_OVERLAY'] = self.options.component_overlay
        cmake.definitions['OGRE_BUILD_COMPONENT_OVERLAY_IMGUI'] = self.options.component_overlay_imgui
        cmake.definitions['OGRE_BUILD_COMPONENT_PYTHON'] = False
        cmake.definitions['OGRE_BUILD_COMPONENT_CSHARP'] = False
        cmake.definitions['OGRE_BUILD_COMPONENT_JAVA'] = False

        cmake.definitions['OGRE_BUILD_PLUGIN_OCTREE'] = self.options.plugin_octree
        cmake.definitions['OGRE_BUILD_PLUGIN_BSP'] = self.options.plugin_bsp
        cmake.definitions['OGRE_BUILD_PLUGIN_CG'] = self.options.plugin_cg
        cmake.definitions['OGRE_BUILD_PLUGIN_EXRCODEC'] = self.options.plugin_exrcodec
        cmake.definitions['OGRE_BUILD_PLUGIN_STBI'] = self.options.plugin_stbi
        cmake.definitions['OGRE_BUILD_PLUGIN_FREEIMAGE'] = self.options.plugin_freeimage
        cmake.definitions['OGRE_BUILD_PLUGIN_PFX'] = self.options.plugin_pfx
        cmake.definitions['OGRE_BUILD_PLUGIN_PCZ'] = self.options.plugin_pcz
        cmake.definitions['OGRE_BUILD_PLUGIN_DOT_SCENE'] = self.options.plugin_dot_scene
        cmake.definitions['OGRE_BUILD_PLUGIN_ASSIMP'] = self.options.plugin_assimp

        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D9'] = self.options.get_safe('rendersystem_d3d9')
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_D3D11'] = self.options.get_safe('rendersystem_d3d11')
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL'] = self.options.rendersystem_gl
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GL3PLUS'] = self.options.rendersystem_gl3plus
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_GLES2'] = self.options.rendersystem_gles2
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_METAL'] = self.options.get_safe('rendersystem_metal')
        cmake.definitions['OGRE_BUILD_RENDERSYSTEM_TINY'] = self.options.get_safe('rendersystem_tiny')

        cmake.definitions['OGRE_BUILD_TESTS'] = False
        cmake.definitions['OGRE_BUILD_TOOLS'] = False
        cmake.definitions['OGRE_BUILD_SAMPLES'] = False
        cmake.definitions['OGRE_BUILD_DEPENDENCIES'] = False
        cmake.definitions['OGRE_COPY_DEPENDENCIES'] = False

        cmake.definitions['OGRE_INSTALL_CMAKE'] = True
        cmake.definitions['OGRE_INSTALL_PDB'] = True
        cmake.definitions['OGRE_INSTALL_DEPENDENCIES'] = False
        cmake.definitions['OGRE_INSTALL_DOCS'] = False
        cmake.definitions['OGRE_INSTALL_TOOLS'] = False
        cmake.definitions['OGRE_INSTALL_SAMPLES'] = False

        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_folder, keep_path=False)

        for config_file in [
            'samples.cfg',
            'tests.cfg',
            'resources.cfg',
        ]:
            if self.settings.os == 'Windows':
                config_file_path = os.path.join(self.package_folder, 'bin', config_file)
            else:
                config_file_path = os.path.join(self.package_folder, 'share', 'OGRE', config_file)

            os.remove(config_file_path)

        if self.settings.os == 'Windows':
            tools.rmdir(os.path.join(self.package_folder, 'Media'))
        else:
            tools.rmdir(os.path.join(self.package_folder, 'share', 'OGRE', 'Media'))
            os.remove(os.path.join(self.package_folder, 'share', 'OGRE', 'GLX_backdrop.png'))

    def package_info(self):
        self.cpp_info.libdirs.append(os.path.join(self.cpp_info.libdirs[0], "OGRE"))

        # Set the name of conan auto generated FindOGRE.cmake.
        self.cpp_info.names["cmake_find_package"] = "OGRE"
        self.cpp_info.names["cmake_find_package_multi"] = "OGRE"

        # Set the package folder as CMAKE_PREFIX_PATH to find OGREConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.component_bites:
            if not any("OgreBites" in s for s in self.cpp_info.libs):
                self.output.warn("OgreBites component as not been built.")
        if self.options.component_paging:
            if not any("OgrePaging" in s for s in self.cpp_info.libs):
                self.output.warn("Paging component as not been built.")
        if self.options.component_meshlodgenerator:
            if not any("OgreMeshLodGenerator" in s for s in self.cpp_info.libs):
                self.output.warn("MeshLodGenerator component as not been built.")
        if self.options.component_property:
            if not any("OgreProperty" in s for s in self.cpp_info.libs):
                self.output.warn("Property component as not been built.")
        if self.options.component_terrain:
            if not any("OgreTerrain" in s for s in self.cpp_info.libs):
                self.output.warn("Terrain component as not been built.")
        if self.options.component_rtshadersystem:
            if not any("OgreRTShaderSystem" in s for s in self.cpp_info.libs):
                self.output.warn("RTShader System component as not been built.")
        if self.options.component_volume:
            if not any("OgreVolume" in s for s in self.cpp_info.libs):
                self.output.warn("Volume component as not been built.")
        if self.options.component_overlay:
            if not any("OgreOverlay" in s for s in self.cpp_info.libs):
                self.output.warn("Overlay component as not been built.")
        if self.options.plugin_octree:
            if not any("Plugin_OctreeSceneManager" in s for s in self.cpp_info.libs):
                self.output.warn("Octree SceneManager plugin as not been built.")
        if self.options.plugin_bsp:
            if not any("Plugin_BSPSceneManager" in s for s in self.cpp_info.libs):
                self.output.warn("BSP SceneManager plugin as not been built.")
        if self.options.plugin_cg:
            if not any("Plugin_CgProgramManager" in s for s in self.cpp_info.libs):
                self.output.warn("Cg plugin as not been built.")
        if self.options.plugin_exrcodec:
            if not any("Codec_EXR" in s for s in self.cpp_info.libs):
                self.output.warn("EXR Codec plugin as not been built.")
        if self.options.plugin_stbi:
            if not any("Codec_STBI" in s for s in self.cpp_info.libs):
                self.output.warn("STBI image codec plugin as not been built.")
        if self.options.plugin_freeimage:
            if not any("Codec_FreeImage" in s for s in self.cpp_info.libs):
                self.output.warn("FreeImage codec plugin as not been built.")
        if self.options.plugin_pfx:
            if not any("Plugin_ParticleFX" in s for s in self.cpp_info.libs):
                self.output.warn("ParticleFX plugin as not been built.")
        if self.options.plugin_pcz:
            if not any("Plugin_PCZSceneManager" in s for s in self.cpp_info.libs):
                self.output.warn("PCZ SceneManager plugin as not been built.")
        if self.options.plugin_dot_scene:
            if not any("Plugin_DotScene" in s for s in self.cpp_info.libs):
                self.output.warn("Dot scene plugin as not been built.")
        if self.options.plugin_assimp:
            if not any("Codec_Assimp" in s for s in self.cpp_info.libs):
                self.output.warn("Assimp plugin as not been built.")
        if self.options.get_safe("rendersystem_d3d9", False):
            if not any("RenderSystem_Direct3D9" in s for s in self.cpp_info.libs):
                self.output.warn("Direct3D9 RenderSystem as not been built.")
        if self.options.get_safe("rendersystem_d3d11", False):
            if not any("RenderSystem_Direct3D11" in s for s in self.cpp_info.libs):
                self.output.warn("Direct3D11 RenderSystem as not been built.")
        if self.options.get_safe("rendersystem_metal", False):
            if not any("RenderSystem_Metal" in s for s in self.cpp_info.libs):
                self.output.warn("Metal RenderSystem as not been built.")
        if self.options.rendersystem_gl:
            if not any("RenderSystem_GL" in s for s in self.cpp_info.libs):
                self.output.warn("OpenGL RenderSystem as not been built.")
        if self.options.rendersystem_gl3plus:
            if not any("RenderSystem_GL3Plus" in s for s in self.cpp_info.libs):
                self.output.warn("OpenGL 3+ RenderSystem as not been built.")
        if self.options.rendersystem_gles2:
            if not any("RenderSystem_GLES2" in s for s in self.cpp_info.libs):
                self.output.warn("GLES 2 RenderSystem as not been built.")
        if self.options.rendersystem_tiny:
            if not any("RenderSystem_Tiny" in s for s in self.cpp_info.libs):
                self.output.warn("Tiny RenderSystem as not been built.")
