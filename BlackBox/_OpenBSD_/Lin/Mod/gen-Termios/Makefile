# This is BSD Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: Termios.txt

PY = python2.7
DEFS = defs-termios

Termios.txt: Termios.txt.templ ${DEFS}
	${PY} ./untempl.py Termios.txt.templ ${.TARGET}

defs-termios: /usr/include/termios.h
	./dumpdefs.py 2 0 i ${.ALLSRC} > ${.TARGET}
	./dumpdefs.py 2 1 i ${.ALLSRC} | grep -v compat >> ${.TARGET}
	./dumpdefs.py 2 2 i ${.ALLSRC} | grep -v compat | grep -v CHWFLOW >> ${.TARGET}

clean:
	rm -f Termios.txt ${DEFS}
