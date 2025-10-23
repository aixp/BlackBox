.PHONY: all clean

CFLAGS += -m32

all: Ioctl.txt

Ioctl.txt: Ioctl.txt.templ defs-basictypes subsystem libver osname machine
	../untempl_h.py -m 32 Ioctl.txt.templ Ioctl.txt

defs-basictypes: sizeofs
	./sizeofs > defs-basictypes

clean:
	rm -f Ioctl.txt sizeofs defs-basictypes
