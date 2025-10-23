.PHONY: all clean

CFLAGS += -m32

DEFS = defs-errno defs-basictypes

all: Libc.txt ${DEFS} strerrnocase.txt

Libc.txt: Libc.txt.templ ${DEFS} subsystem libver osname machine custom fields-dirent fields-sigaction fields-siginfo fields-stack fields-stat fields-tm fields-ucontext fields-timespec
	../untempl_h.py -m 32 Libc.txt.templ Libc.txt

defs-errno.txt: defs-errno.txt.templ
	../untempl_h.py -m 32 defs-errno.txt.templ defs-errno.txt

defs-errno: defs-errno.txt
	cat defs-errno.txt | awk '{print $$1}' | sed s'/*//' > defs-errno

defs-basictypes: sizeofs
	./sizeofs > defs-basictypes

dumpstrerrno.c: defs-errno
	grep -v ERESTART defs-errno | grep -v EJUSTRETURN | ./mkdumpstrerrno.py > dumpstrerrno.c

strerrnocase.txt: dumpstrerrno
	./dumpstrerrno | ./mkstrerrnocase.py > strerrnocase.txt

clean:
	rm -f ${DEFS} Libc.txt dumpstrerrno dumpstrerrno.c strerrnocase.txt sizeofs defs-errno.txt
