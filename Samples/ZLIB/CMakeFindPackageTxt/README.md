# ZLIB cmake_find_package conanfile.txt sample

this samples show how to use ZLIB with a conanfile.txt and the cmake_find_package generator.

### Generation

```
> conan install -if ./build .
> cmake -S . -B ./build
> cmake --build ./build
```