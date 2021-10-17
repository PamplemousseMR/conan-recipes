import os
from conans import ConanFile, tools, CMake

class AssimpConan(ConanFile):
    name = "assimp"
    description = "The official Open-Asset-Importer-Library Repository. Loads 40+ 3D-file-formats into one unified and clean data structure"
    homepage = "https://github.com/assimp/assimp"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "BSD-3-Clause"
    author = "MANCIAUX Romain (https://github.com/PamplemousseMR)"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "double_precision": [True, False],
        "with_3d": [True, False],
        "with_3ds": [True, False],
        "with_3ds_exporter": [True, False],
        "with_3mf": [True, False],
        "with_3mf_exporter": [True, False],
        "with_ac": [True, False],
        "with_amf": [True, False],
        "with_ase": [True, False],
        "with_assbin": [True, False],
        "with_assbin_exporter": [True, False],
        "with_assxml_exporter": [True, False],
        "with_assjson_exporter": [True, False],
        "with_b3d": [True, False],
        "with_blend": [True, False],
        "with_bvh": [True, False],
        "with_ms3d": [True, False],
        "with_cob": [True, False],
        "with_collada": [True, False],
        "with_collada_exporter": [True, False],
        "with_csm": [True, False],
        "with_dxf": [True, False],
        "with_fbx": [True, False],
        "with_fbx_exporter": [True, False],
        "with_gltf": [True, False],
        "with_gltf_exporter": [True, False],
        "with_hmp": [True, False],
        "with_ifc": [True, False],
        "with_irr": [True, False],
        "with_irrmesh": [True, False],
        "with_lwo": [True, False],
        "with_lws": [True, False],
        "with_md2": [True, False],
        "with_md3": [True, False],
        "with_md5": [True, False],
        "with_mdc": [True, False],
        "with_mdl": [True, False],
        "with_mmd": [True, False],
        "with_ndo": [True, False],
        "with_nff": [True, False],
        "with_obj": [True, False],
        "with_obj_exporter": [True, False],
        "with_off": [True, False],
        "with_ogre": [True, False],
        "with_opengex": [True, False],
        "with_opengex_exporter": [True, False],
        "with_ply": [True, False],
        "with_ply_exporter": [True, False],
        "with_q3bsp": [True, False],
        "with_q3d": [True, False],
        "with_raw": [True, False],
        "with_sib": [True, False],
        "with_smd": [True, False],
        "with_step": [True, False],
        "with_step_exporter": [True, False],
        "with_stl": [True, False],
        "with_stl_exporter": [True, False],
        "with_terragen": [True, False],
        "with_x": [True, False],
        "with_x_exporter": [True, False],
        "with_x3d": [True, False],
        "with_x3d_exporter": [True, False],
        "with_xgl": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "double_precision": False,
        "with_3d": True,
        "with_3ds": True,
        "with_3ds_exporter": True,
        "with_3mf": True,
        "with_3mf_exporter": False, # Need kuba_zip
        "with_ac": True,
        "with_amf": True,
        "with_ase": True,
        "with_assbin": True,
        "with_assbin_exporter": True,
        "with_assxml_exporter": True,
        "with_assjson_exporter": True,
        "with_b3d": True,
        "with_blend": False, # Need poly2tri
        "with_bvh": True,
        "with_ms3d": True,
        "with_cob": True,
        "with_collada": True,
        "with_collada_exporter": True,
        "with_csm": True,
        "with_dxf": True,
        "with_fbx": True,
        "with_fbx_exporter": True,
        "with_gltf": False, # Need rapidjson
        "with_gltf_exporter": False, # Need rapidjson
        "with_hmp": True,
        "with_ifc": False, # Need poly2tri
        "with_irr": True,
        "with_irrmesh": True,
        "with_lwo": True,
        "with_lws": True,
        "with_md2": True,
        "with_md3": True,
        "with_md5": True,
        "with_mdc": True,
        "with_mdl": True,
        "with_mmd": True,
        "with_ndo": True,
        "with_nff": True,
        "with_obj": True,
        "with_obj_exporter": True,
        "with_off": True,
        "with_ogre": True,
        "with_opengex": True,
        "with_opengex_exporter": True,
        "with_ply": True,
        "with_ply_exporter": True,
        "with_q3bsp": True,
        "with_q3d": True,
        "with_raw": True,
        "with_sib": True,
        "with_smd": True,
        "with_step": True,
        "with_step_exporter": True,
        "with_stl": True,
        "with_stl_exporter": True,
        "with_terragen": True,
        "with_x": True,
        "with_x_exporter": True,
        "with_x3d": True,
        "with_x3d_exporter": True,
        "with_xgl": True,
    }
    exports_sources = "CMakeLists.txt"
    short_paths = True

    _source_folder = "{0}_sources".format(name)
    _build_folder = "{0}_build".format(name)

    @property
    def _depends_on_kuba_zip(self):
        return self.options.with_3mf_exporter

    @property
    def _depends_on_poly2tri(self):
        return self.options.with_blend or self.options.with_ifc

    @property
    def _depends_on_rapidjson(self):
        return self.options.with_gltf or self.options.with_gltf_exporter

    @property
    def _depends_on_zlib(self):
        return self.options.with_assbin or self.options.with_assbin_exporter or \
               self.options.with_assxml_exporter or self.options.with_blend or self.options.with_fbx or \
               self.options.with_q3bsp or self.options.with_x or self.options.with_xgl

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def requirements(self):
        for requirement in self.conan_data["requirements"][self.version]:
            self.requires.add("{0}@{1}/{2}".format(requirement, self.user, self.channel))
        
        if self._depends_on_kuba_zip:
            self.requires.add("kuba-zip/{0}@{1}/{2}".format(self.conan_data["kuba-zip"][self.version], self.user, self.channel))

        if self._depends_on_poly2tri:
            self.requires.add("poly2tri/{0}@{1}/{2}".format(self.conan_data["poly2tri"][self.version], self.user, self.channel))

        if self._depends_on_rapidjson:
            self.requires.add("rapidjson/{0}@{1}/{2}".format(self.conan_data["rapidjson"][self.version], self.user, self.channel))

        if self._depends_on_zlib:
            self.requires.add("zlib/{0}@{1}/{2}".format(self.conan_data["zlib"][self.version], self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["HUNTER_ENABLED"] = False
        cmake.definitions["ASSIMP_NO_EXPORT"] = False
        cmake.definitions["ASSIMP_BUILD_ASSIMP_TOOLS"] = False
        cmake.definitions["ASSIMP_BUILD_TESTS"] = False
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = False
        cmake.definitions["ASSIMP_ANDROID_JNIIOSYSTEM"] = False
        cmake.definitions["ASSIMP_INSTALL_PDB"] = False
        cmake.definitions["SYSTEM_IRRXML"] = True
        cmake.definitions["IGNORE_GIT_HASH"] = True
        cmake.definitions["ASSIMP_BUILD_ALL_IMPORTERS_BY_DEFAULT"] = False
        cmake.definitions["ASSIMP_BUILD_ALL_EXPORTERS_BY_DEFAULT"] = False
        cmake.definitions["ASSIMP_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.definitions["ASSIMP_BUILD_3D_IMPORTER"] = self.options.with_3d
        cmake.definitions["ASSIMP_BUILD_3DS_IMPORTER"] = self.options.with_3ds
        cmake.definitions["ASSIMP_BUILD_3DS_EXPORTER"] = self.options.with_3ds_exporter
        cmake.definitions["ASSIMP_BUILD_3MF_IMPORTER"] = self.options.with_3mf
        cmake.definitions["ASSIMP_BUILD_3MF_EXPORTER"] = self.options.with_3mf_exporter
        cmake.definitions["ASSIMP_BUILD_AC_IMPORTER"] = self.options.with_ac
        cmake.definitions["ASSIMP_BUILD_AMF_IMPORTER"] = self.options.with_amf
        cmake.definitions["ASSIMP_BUILD_ASE_IMPORTER"] = self.options.with_ase
        cmake.definitions["ASSIMP_BUILD_ASSBIN_IMPORTER"] = self.options.with_assbin
        cmake.definitions["ASSIMP_BUILD_ASSBIN_EXPORTER"] = self.options.with_assbin_exporter
        cmake.definitions["ASSIMP_BUILD_ASSXML_EXPORTER"] = self.options.with_assxml_exporter
        cmake.definitions["ASSIMP_BUILD_ASSJSON_EXPORTER"] = self.options.with_assjson_exporter
        cmake.definitions["ASSIMP_BUILD_B3D_IMPORTER"] = self.options.with_b3d
        cmake.definitions["ASSIMP_BUILD_BLEND_IMPORTER"] = self.options.with_blend
        cmake.definitions["ASSIMP_BUILD_BVH_IMPORTER"] = self.options.with_bvh
        cmake.definitions["ASSIMP_BUILD_MS3D_IMPORTER"] = self.options.with_ms3d
        cmake.definitions["ASSIMP_BUILD_COB_IMPORTER"] = self.options.with_cob
        cmake.definitions["ASSIMP_BUILD_COLLADA_IMPORTER"] = self.options.with_collada
        cmake.definitions["ASSIMP_BUILD_COLLADA_EXPORTER"] = self.options.with_collada_exporter
        cmake.definitions["ASSIMP_BUILD_CSM_IMPORTER"] = self.options.with_csm
        cmake.definitions["ASSIMP_BUILD_DXF_IMPORTER"] = self.options.with_dxf
        cmake.definitions["ASSIMP_BUILD_FBX_IMPORTER"] = self.options.with_fbx
        cmake.definitions["ASSIMP_BUILD_FBX_EXPORTER"] = self.options.with_fbx_exporter
        cmake.definitions["ASSIMP_BUILD_GLTF_IMPORTER"] = self.options.with_gltf
        cmake.definitions["ASSIMP_BUILD_GLTF_EXPORTER"] = self.options.with_gltf_exporter
        cmake.definitions["ASSIMP_BUILD_HMP_IMPORTER"] = self.options.with_hmp
        cmake.definitions["ASSIMP_BUILD_IFC_IMPORTER"] = self.options.with_ifc
        cmake.definitions["ASSIMP_BUILD_IRR_IMPORTER"] = self.options.with_irr
        cmake.definitions["ASSIMP_BUILD_IRRMESH_IMPORTER"] = self.options.with_irrmesh
        cmake.definitions["ASSIMP_BUILD_LWO_IMPORTER"] = self.options.with_lwo
        cmake.definitions["ASSIMP_BUILD_LWS_IMPORTER"] = self.options.with_lws
        cmake.definitions["ASSIMP_BUILD_MD2_IMPORTER"] = self.options.with_md2
        cmake.definitions["ASSIMP_BUILD_MD3_IMPORTER"] = self.options.with_md3
        cmake.definitions["ASSIMP_BUILD_MD5_IMPORTER"] = self.options.with_md5
        cmake.definitions["ASSIMP_BUILD_MDC_IMPORTER"] = self.options.with_mdc
        cmake.definitions["ASSIMP_BUILD_MDL_IMPORTER"] = self.options.with_mdl
        cmake.definitions["ASSIMP_BUILD_MMD_IMPORTER"] = self.options.with_mmd
        cmake.definitions["ASSIMP_BUILD_NDO_IMPORTER"] = self.options.with_ndo
        cmake.definitions["ASSIMP_BUILD_NFF_IMPORTER"] = self.options.with_nff
        cmake.definitions["ASSIMP_BUILD_OBJ_IMPORTER"] = self.options.with_obj
        cmake.definitions["ASSIMP_BUILD_OBJ_EXPORTER"] = self.options.with_obj_exporter
        cmake.definitions["ASSIMP_BUILD_OFF_IMPORTER"] = self.options.with_off
        cmake.definitions["ASSIMP_BUILD_OGRE_IMPORTER"] = self.options.with_ogre
        cmake.definitions["ASSIMP_BUILD_OPENGEX_IMPORTER"] = self.options.with_opengex
        cmake.definitions["ASSIMP_BUILD_OPENGEX_EXPORTER"] = self.options.with_opengex_exporter
        cmake.definitions["ASSIMP_BUILD_PLY_IMPORTER"] = self.options.with_ply
        cmake.definitions["ASSIMP_BUILD_PLY_EXPORTER"] = self.options.with_ply_exporter
        cmake.definitions["ASSIMP_BUILD_Q3BSP_IMPORTER"] = self.options.with_q3bsp
        cmake.definitions["ASSIMP_BUILD_Q3D_IMPORTER"] = self.options.with_q3d
        cmake.definitions["ASSIMP_BUILD_RAW_IMPORTER"] = self.options.with_raw
        cmake.definitions["ASSIMP_BUILD_SIB_IMPORTER"] = self.options.with_sib
        cmake.definitions["ASSIMP_BUILD_SMD_IMPORTER"] = self.options.with_smd
        cmake.definitions["ASSIMP_BUILD_STEP_IMPORTER"] = self.options.with_step
        cmake.definitions["ASSIMP_BUILD_STEP_EXPORTER"] = self.options.with_step_exporter
        cmake.definitions["ASSIMP_BUILD_STL_IMPORTER"] = self.options.with_stl
        cmake.definitions["ASSIMP_BUILD_STL_EXPORTER"] = self.options.with_stl_exporter
        cmake.definitions["ASSIMP_BUILD_TERRAGEN_IMPORTER"] = self.options.with_terragen
        cmake.definitions["ASSIMP_BUILD_X_IMPORTER"] = self.options.with_x
        cmake.definitions["ASSIMP_BUILD_X_EXPORTER"] = self.options.with_x_exporter
        cmake.definitions["ASSIMP_BUILD_X3D_IMPORTER"] = self.options.with_x3d
        cmake.definitions["ASSIMP_BUILD_X3D_EXPORTER"] = self.options.with_x3d_exporter
        cmake.definitions["ASSIMP_BUILD_XGL_IMPORTER"] = self.options.with_xgl

        cmake.configure(build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

        # Remove the pkg config, it contains absolute paths. Let conan generate them.
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

        if self.settings.build_type == "Release":
            os.remove(os.path.join(self.package_folder, "lib", "cmake", "assimp-5.0", "assimpTargets-debug.cmake"))
        else:
            os.remove(os.path.join(self.package_folder, "lib", "cmake", "assimp-5.0", "assimpTargets-release.cmake"))

    def package_info(self):
        # Name of the find package file: Findassimp.cmake
        self.cpp_info.filenames["cmake_find_package"] = "assimp"
        self.cpp_info.filenames["cmake_find_package_multi"] = "assimp"

        # name of the target: assimp::assimp
        self.cpp_info.name = "assimp"
        self.cpp_info.names["pkg_config"] = "assimp"

        # Libraries
        self.cpp_info.libs = tools.collect_libs(self)

        if tools.os_info.is_linux:
            self.cpp_info.system_libs.extend(["rt", "m", "pthread"])