# This is BSD Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: mkioctl Ioctl.txt

PY = python2.7
DEFS = defs-ttycom defs-ioctl

defs-ioctl: mkioctl
	./mkioctl > ${.TARGET}

Ioctl.txt: Ioctl.txt.templ ${DEFS}
	${PY} ./untempl.py Ioctl.txt.templ ${.TARGET}

defs-ttycom: /usr/include/sys/ttycom.h
	./dumpdefs.py 3 1 s ${.ALLSRC} | grep TIOCM_ > ${.TARGET}

clean:
	rm -f mkioctl Ioctl.txt ${DEFS}
