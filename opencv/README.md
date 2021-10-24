# conan-opencv

conan recipes for OpenCV.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Generation

Generate using conan: `conan create . <USER>/<CHANNEL> [-o OPTIONS]`.
```
USER:
	This term in a Conan reference is basically a namespace to avoid collisions of libraries with the same
	name and version in the local cache and in the same remote. This field is usually populated with the
	author’s name of the package recipe (which could be different from the author of the library itself)
	or with the name of the organization creating it.

CHANNEL:
	Normally, package creators use `testing` when developing a recipe (e.g. it compiles only in few
	configurations) and `stable` when the recipe is ready enough to be used (e.g. it is built and tested
	in a wide range of configurations).

OPTIONS: 
	- opencv:shared={'True'|'False'}
		Set to 'True' to build shared library, default to 'False'.
	- opencv:fPIC={'True'|'False'}
		Set to 'True' to build position independent code, default to 'True'.	
	- opencv:with_png={'True'|'False'}
		Set to 'True' to include PNG support, default to 'False'.
	- opencv:parallel={'False'|'tbb'|'openmp'}
		Set parallel computation mode, default to 'False'.
	- opencv:with_cuda={'True'|'False'}
		Set to 'True' to include NVidia Cuda runtime support, default to 'False'.
	- opencv:with_cublas={'True'|'False'}
		Set to 'True' to include NVidia Cuda basic linear algebra subprograms (BLAS) library support, default to 'False'.
	- opencv:with_protobuf={'True'|'False'}
		Set to 'True' to enable libprotobuf, default to 'False'.
	- opencv:with_cudnn={'True'|'False'}
		Set to 'True' to include NVIDIA CUDA deep neural network (cuDNN) library support, default to 'False'.
	- opencv:contrib={'True'|'False'}
		Set to 'True' to add additional OpenCV modules, default to 'False'.
```

## Authors

* **MANCIAUX Romain** - *Initial work* - [PamplemousseMR](https://github.com/PamplemousseMR).

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.