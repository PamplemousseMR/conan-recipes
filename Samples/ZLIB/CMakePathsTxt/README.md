
# ZLIB cmake_paths conanfile.txt sample

this samples show how to use ZLIB with a conanfile.txt and the cmake_paths generator.

### Generation

Included using the CMAKE_PROJECT_\<PROJECT-NAME\>_INCLUDE

```
> conan install -if ./build .
> cmake -S . -B ./build -DCMAKE_PROJECT_test_package_INCLUDE=.\build\conan_paths.cmake
> cmake --build ./build
```

Included as a toolchain

```
> conan install -if ./build .
> cmake -S . -B ./build -DCMAKE_TOOLCHAIN_FILE=.\build\conan_paths.cmake
> cmake --build ./build
```