import os
from conans import ConanFile, tools, CMake


class OpenCVConan(ConanFile):
    name = "opencv"
    version = "4.5.1"
    description = "Open Source Computer Vision Library"
    homepage = "https://github.com/opencv/opencv"
    url = "https://github.com/PamplemousseMR/conan-recipes"
    license = "Apache"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_png": [True, False],
        "parallel": [False, "tbb", "openmp"],
        "with_cuda": [True, False],
        "with_cublas": [True, False],
        "with_protobuf": [True, False],
        "with_cudnn": [True, False],
        "contrib": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_png": False,
        "parallel": False,
        "with_cuda": False,
        "with_cublas": False,
        "with_protobuf": False,
        "with_cudnn": False,
        "contrib": False
    }
    short_paths = True

    _source_folder = "{0}-{1}_sources".format(name, version)
    _contrib_folder = "{0}-{1}_contrib".format(name, version)
    _build_folder = "{0}-{1}_build".format(name, version)

    def config_options(self):
        if tools.os_info.is_windows:
            del self.options.fPIC

    def configure(self):
        if self.options.with_cublas and not self.options.with_cuda:
            self.output.warn("with_cublas option needs with_cuda option to be built. The option is disable")
            self.options.with_cublas = False

        if self.options.with_cudnn and not(self.options.with_cuda and self.options.with_cublas and self.options.with_protobuf):
            self.output.warn("with_cudnn option needs with_cuda, with_cublas and with_protobuf options to be built. The option is disable")
            self.options.with_cudnn = False

    def requirements(self):
        if self.options.with_png:
            self.requires.add("libpng/1.6.37@{0}/{1}".format(self.user, self.channel))

        if self.options.with_protobuf:
            self.requires.add("protobuf/3.13.0@{0}/{1}".format(self.user, self.channel))

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="e27fe5b168918ab60d58d7ace2bd82dd14a4d0bd1d3ae182952c2113f5637513")
        os.rename("{0}-{1}".format(self.name, self.version), self._source_folder)

        if self.options.contrib:
            tools.get("{0}_contrib/archive/{1}.tar.gz".format(self.homepage, self.version),
                      sha256="12c3b1ddd0b8c1a7da5b743590a288df0934e5cef243e036ca290c2e45e425f5")
            os.rename("{0}_contrib-{1}".format(self.name, self.version), self._contrib_folder)

    def build(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_CUDA_STUBS"] = False
        cmake.definitions["BUILD_DOCS"] = False
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_FAT_JAVA_LIB"] = False
        cmake.definitions["BUILD_IPP_IW"] = False
        cmake.definitions["BUILD_ITT"] = False
        cmake.definitions["BUILD_JASPER"] = False
        cmake.definitions["BUILD_JAVA"] = False
        cmake.definitions["BUILD_JPEG"] = False
        cmake.definitions["BUILD_OPENEXR"] = False
        cmake.definitions["BUILD_OPENJPEG"] = False
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["BUILD_PROTOBUF"] = False
        cmake.definitions["BUILD_PACKAGE"] = False
        cmake.definitions["BUILD_PERF_TESTS"] = False
        cmake.definitions["BUILD_USE_SYMLINKS"] = False
        cmake.definitions["BUILD_opencv_apps"] = False
        cmake.definitions["BUILD_opencv_java"] = False
        cmake.definitions["BUILD_opencv_java_bindings_gen"] = False
        cmake.definitions["BUILD_opencv_js"] = False
        cmake.definitions["BUILD_ZLIB"] = False
        cmake.definitions["BUILD_PNG"] = False
        cmake.definitions["BUILD_TIFF"] = False
        cmake.definitions["BUILD_WEBP"] = False
        cmake.definitions["BUILD_TBB"] = False
        cmake.definitions["OPENCV_FORCE_3RDPARTY_BUILD"] = False
        cmake.definitions["BUILD_opencv_python2"] = False
        cmake.definitions["BUILD_opencv_python3"] = False
        cmake.definitions["BUILD_opencv_python_bindings_g"] = False
        cmake.definitions["BUILD_opencv_python_tests"] = False
        cmake.definitions["BUILD_opencv_ts"] = False

        cmake.definitions["WITH_1394"] = False
        cmake.definitions["WITH_ADE"] = False
        cmake.definitions["WITH_ARAVIS"] = False
        cmake.definitions["WITH_CLP"] = False
        cmake.definitions["WITH_CUDA"] = self.options.with_cuda
        cmake.definitions["WITH_CUFFT"] = False
        cmake.definitions["WITH_CUDNN"] = self.options.with_cudnn
        cmake.definitions["WITH_CUBLAS"] = self.options.with_cublas
        cmake.definitions["WITH_NVCUVID"] = False
        cmake.definitions["WITH_FFMPEG"] = False
        cmake.definitions["WITH_GSTREAMER"] = False
        cmake.definitions["WITH_HALIDE"] = False
        cmake.definitions["WITH_HPX"] = False
        cmake.definitions["WITH_IMGCODEC_HDR"] = False
        cmake.definitions["WITH_IMGCODEC_PFM"] = False
        cmake.definitions["WITH_IMGCODEC_PXM"] = False
        cmake.definitions["WITH_IMGCODEC_SUNRASTER"] = False
        cmake.definitions["WITH_INF_ENGINE"] = False
        cmake.definitions["WITH_IPP"] = False
        cmake.definitions["WITH_ITT"] = False
        cmake.definitions["WITH_LIBREALSENSE"] = False
        cmake.definitions["WITH_MFX"] = False
        cmake.definitions["WITH_NGRAPH"] = False
        cmake.definitions["WITH_OPENCL"] = False
        cmake.definitions["WITH_OPENCLAMDBLAS"] = False
        cmake.definitions["WITH_OPENCLAMDFFT"] = False
        cmake.definitions["WITH_OPENCL_SVM"] = False
        cmake.definitions["WITH_OPENGL"] = False
        cmake.definitions["WITH_OPENJPEG"] = False
        cmake.definitions["WITH_OPENMP"] = False
        cmake.definitions["WITH_OPENNI"] = False
        cmake.definitions["WITH_OPENNI2"] = False
        cmake.definitions["WITH_OPENVX"] = False
        cmake.definitions["WITH_PLAIDML"] = False
        cmake.definitions["WITH_PNG"] = self.options.with_png
        cmake.definitions["WITH_PROTOBUF"] = self.options.with_protobuf
        cmake.definitions["WITH_PVAPI"] = False
        cmake.definitions["WITH_QT"] = False
        cmake.definitions["WITH_QUIRC"] = False
        cmake.definitions["WITH_V4L"] = False
        cmake.definitions["WITH_VA"] = False
        cmake.definitions["WITH_VA_INTEL"] = False
        cmake.definitions["WITH_VTK"] = False
        cmake.definitions["WITH_VULKAN"] = False
        cmake.definitions["WITH_XIMEA"] = False
        cmake.definitions["WITH_XINE"] = False
        cmake.definitions["WITH_LAPACK"] = False

        cmake.definitions["ENABLE_PIC"] = self.options.get_safe("fPIC", True)

        if self.options.parallel:
            cmake.definitions["WITH_TBB"] = self.options.parallel == "tbb"
            cmake.definitions["WITH_OPENMP"] = self.options.parallel == "openmp"

        if self.options.contrib:
            cmake.definitions['OPENCV_EXTRA_MODULES_PATH'] = os.path.join(self.build_folder, self._contrib_folder, 'modules')

        if self.settings.compiler == "Visual Studio":
            cmake.definitions["BUILD_WITH_STATIC_CRT"] = "MT" in str(self.settings.compiler.runtime)

        if self.options.with_protobuf:
            cmake.definitions["PROTOBUF_UPDATE_FILES"] = True

        cmake.configure(source_folder=self._source_folder, build_folder=self._build_folder)
        cmake.build()
        cmake.install()

    def package(self):
        # Copying the license file.
        self.copy("LICENSE", src=self._source_folder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # Set the name of conan auto generated FindOpenCV.cmake.
        self.cpp_info.names["cmake_find_package"] = "OpenCV"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenCV"

        # Set the name of conan auto generated opencv.pc.
        self.cpp_info.names["pkg_config"] = "OpenCV"

        # Set the package folder as CMAKE_PREFIX_PATH to find OpenCVConfig.cmake.
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
