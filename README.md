# [Oberon Microsystems](http://www.oberon.ch/) [BlackBox Component Builder](https://en.wikipedia.org/wiki/BlackBox_Component_Builder) [1.6](https://blackboxframework.org/stable/SetupBlackBox16.exe)
# Port for OpenBSD/i386, GNU/Linux/i386, FreeBSD/i386

## Tested on

* Arch Linux
* OpenBSD 7.7
* Fedora Core 17
* Ubuntu 12.04 LTS, 12.10, 13.10, 14.04
* FreeBSD 14.3

## Install build dependencies

Ubuntu:

```sh
sudo apt-get install libc6-dev-i386
```

## Build

Switch tree to current OS:

```sh
cd BlackBox
./clean
./switch-target $(uname -s) configuration
```

Configurations available: `CLI`, `GUI`

Compile `exe.img` (required for DevBootLinker):

```sh
cd BlackBox/Dev/Rsrc
make clean
make
cp exe.img ../../_$(uname -s)_/Dev/Rsrc/
```

Build the framework:

```sh
cd BlackBox
./build
```

Create the standalone development bundle (`dev`):

```sh
cd BlackBox
./pack-dev
```

`dev` is a self-contained executable including compiler, linker, and other essential tools required to bootstrap the build process.

## Install runtime dependencies

Ubuntu:

```sh
sudo apt-get install libgtk2.0-0:i386
```

OpenBSD:

```sh
doas pkg_add libiconv gtk+2
```

## Run

```sh
cd BlackBox
./run-BlackBox
```
