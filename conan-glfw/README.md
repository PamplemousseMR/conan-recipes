# conan-glfw

conan recipes for glfw.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites for linux

- [Xrandr](https://www.x.org/wiki/libraries/libxrandr/) : A command-line tool to interact with the X RandR extension.
- [Xrender](https://en.wikipedia.org/wiki/X_Rendering_Extension) : An extension to the X11 core protocol to implement image compositing in the X server, to allow an efficient display of transparent images.
- [Xi](https://www.x.org/wiki/) : Provides an X Window System client interface to the XINPUT extension to the X protocol.
- [Xinerama](https://en.wikipedia.org/wiki/Xinerama) : An extension to the X Window System that enables X applications and window managers to use two or more physical displays as one large virtual display.
- [Xcursor](https://www.x.org/releases/X11R7.7/doc/man/man3/Xcursor.3.xhtml) : A simple library designed to help locate and load cursors.
- [OpenGL](https://www.opengl.org/) : An environment for developing portable, interactive 2D and 3D graphics applications.
- [m](https://en.wikipedia.org/wiki/C_mathematical_functions) : A group of functions in the standard library of the C programming language implementing basic mathematical functions.
- [dl](https://docs.oracle.com/cd/E86824_01/html/E54772/libdl-3lib.html) : Dnamic linking library.
- [drm](https://en.wikipedia.org/wiki/Direct_Rendering_Manager) : A subsystem of the Linux kernel, interfaces with the GPUs of modern video cards.
- [Xdamage](https://www.freedesktop.org/wiki/Software/XDamage/) :  Allows applications to track modified regions of drawables.
- [X11-xcb]https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [xcb-glx](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [xcb-dri2](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [xcb-dri3](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [xcb-present](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [xcb-sync](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [Xxf86vm](https://packages.debian.org/fr/sid/libxxf86vm-dev) : An interface to the XFree86-VidModeExtension extension.
- [Xfixes](https://en.wikipedia.org/wiki/XFixes) : An X Window System extension which makes useful additions to the X11 protocol.
- [Xext](https://en.wikipedia.org/wiki/XCB) : A library implementing the client-side of the X11 display server protocol.
- [X11](https://en.wikipedia.org/wiki/XCB) : A subsystem of the Linux kernel, interfaces with the GPUs of modern video cards.
- [pthread](https://en.wikipedia.org/wiki/POSIX_Threads) : A library providing an API that allows to control multiple different flows of work that overlap in time.
- [xcb](https://en.wikipedia.org/wiki/XCB) : Alibrary implementing the client-side of the X11 display server protocol.
- [Xau](https://www.x.org/releases/X11R7.7/doc/man/man3/Xau.3.xhtml) : A library that implements the X11 Authorization protocol.

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
	- glfw:shared={'True'|'False'}
		Set to 'True' to build shared library, default to 'False'.
	- glfw:fPIC={'True'|'False'}
		Set to 'True' to build position independent code, default to 'True'.
```

## Authors

* **MANCIAUX Romain** - *Initial work* - [PamplemousseMR](https://github.com/PamplemousseMR).

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.