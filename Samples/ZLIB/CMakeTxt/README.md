# ZLIB cmake conanfile.txt sample

this samples show how to use zlib with a conanfile.txt and the cmake generator.

### Generation

```
> conan install -if ./build .
> cmake -S . -B ./build
> cmake --build ./build
```