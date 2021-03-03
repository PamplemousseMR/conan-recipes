# BZip2 cmake conanfile.txt sample

this samples show how to use bzip2 with a conanfile.txt and the cmake generator.

### Generation

```
> conan install -if ./build .
> cmake -S . -B ./build
> cmake --build ./build
```