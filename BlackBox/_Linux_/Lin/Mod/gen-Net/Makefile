# This is GNU Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: Net.txt dumphstrerrno

PY = python2.7
DEFS = defs-socket defs-so

Net.txt: Net.txt.templ ${DEFS} defs-netdb defs-in defs-sock
	${PY} ./untempl.py Net.txt.templ $@

defs-socket: /usr/include/i386-linux-gnu/bits/socket.h
	./dumpdefs.py 3 1 i $^ | grep "	PF_" > $@
	./dumpdefs.py 3 1 i $^ | grep "	SOMAXCONN" >> $@

defs-so: /usr/include/asm-generic/socket.h
	./dumpdefs.py 3 1 s $^ | grep "	SO_" > $@

clean:
	rm -f Net.txt ${DEFS} dumphstrerrno
