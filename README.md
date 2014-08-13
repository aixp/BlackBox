[Oberon Microsystems](http://www.oberon.ch/) [BlackBox Component Builder](http://www.oberon.ch/blackbox.html)

Port for OpenBSD/i386, GNU/Linux/i386, FreeBSD/i386

Tested on:
* OpenBSD 5.6
* Fedora Core 17
* Ubuntu 12.04 LTS, 12.10, 13.10, 14.04
* FreeBSD 9.0 (non-GUI part only)

Status:
* non-GUI part: stable, but [TODO](TODO) list is not empty
* GUI part: incomplete, but runnable implementation

How to build:

	if you have 64-bit version of Ubuntu, do this:
		sudo apt-get install libc6-dev-i386

	cd BlackBox
	./clean
	./switch-target `uname -s` [ GUI ]

	compile loader executable:
		cd BlackBox/Lin/Rsrc/loader
		make clean
		make
		mv loader ../../../_`uname -s`_/Lin/Rsrc/loader/

	compile self:
		cd BlackBox
		./build
		./pack-dev0

How to run (after build):

	if you have 64-bit version of Ubuntu and want to run GUI version, do this:
		sudo apt-get install libgtk2.0-0:i386

	cd BlackBox
	./run-BlackBox

Alexander V. Shiryaev, 2014
