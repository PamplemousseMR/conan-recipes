# conan-ogre

conan recipes for Ogre.

## Travis

[![Build Status](https://travis-ci.com/PamplemousseMR/conan-ogre.svg?branch=master)](https://travis-ci.com/PamplemousseMR/conan-ogre)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Generation

Generate using conan: `conan create . <USER>/<CHANNEL>`.
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
```

## Authors

* **MANCIAUX Romain** - *Initial work* - [PamplemousseMR](https://github.com/PamplemousseMR).

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.