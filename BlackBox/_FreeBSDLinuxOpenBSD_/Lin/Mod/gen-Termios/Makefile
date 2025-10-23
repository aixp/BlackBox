.PHONY: all clean

CFLAGS += -m32

all: Termios.txt

Termios.txt: Termios.txt.templ defs-basictypes fields-termios subsystem libver osname machine
	../untempl_h.py -m 32 Termios.txt.templ Termios.txt

defs-basictypes: sizeofs
	./sizeofs > defs-basictypes

clean:
	rm -f Termios.txt sizeofs defs-basictypes
