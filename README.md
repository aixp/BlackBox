# [Oberon Microsystems](http://www.oberon.ch/) [BlackBox Component Builder](https://en.wikipedia.org/wiki/BlackBox_Component_Builder) [1.6](https://blackboxframework.org/stable/SetupBlackBox16.exe)
# Port for OpenBSD/i386, GNU/Linux/i386, FreeBSD/i386

## Tested on

* OpenBSD 6.2
* Fedora Core 17
* Ubuntu 12.04 LTS, 12.10, 13.10, 14.04
* FreeBSD 11.0

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
./switch-target $(uname -s) variant
```

Variants available:

* `Interp`: command-line interpreter
* `GUI`: GUI version

Compile DevElfLinker16 ELF `.so` loader executable:

```sh
cd BlackBox/Lin/Rsrc/loader
make clean
make
mv loader ../../../_$(uname -s)_/Lin/Rsrc/loader/
```

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

Create the standalone development bundle (`dev0`):

```sh
cd BlackBox
./pack-dev0
```

`dev0` is a self-contained executable including compiler, linker, and other essential tools required to bootstrap the build process.

## Install runtime dependencies

Ubuntu:

```sh
sudo apt-get install libgtk2.0-0:i386
```

## Run

There are 3 methods to run the framework:

1. DevElfLinker16-based:

```sh
cd BlackBox
./run-BlackBox
```

2. Dev2Linker-based:

```sh
cd BlackBox
./run-BlackBox1
```

3. DevBootLinker-based:

```sh
cd BlackBox
./run-BlackBox2
```

## Authors

Alexander Shiryaev, 2025
