# This is BSD Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: Net.txt dumphstrerrno

PY = python2.7
DEFS = defs-socket defs-in defs-netdb

Net.txt: Net.txt.templ ${DEFS}
	${PY} ./untempl.py Net.txt.templ ${.TARGET}

defs-socket: /usr/include/sys/socket.h
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	SOCK_" > ${.TARGET}
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	AF_" >> ${.TARGET}
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	SHUT_" >> ${.TARGET}
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	SOMAXCONN" >> ${.TARGET}
	./dumpdefs.py 3 1 s ${.ALLSRC} | grep "	SO_" >> ${.TARGET}
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	SOL_" >> ${.TARGET}
	./dumpdefs.py 3 1 s ${.ALLSRC} | grep "	MSG_" >> ${.TARGET}

defs-in: /usr/include/netinet/in.h
	./dumpdefs.py 3 1 i ${.ALLSRC} | grep "	IPPROTO_" > ${.TARGET}

defs-netdb: /usr/include/netdb.h
	./dumpdefs.py 3 2 i ${.ALLSRC} > ${.TARGET}

clean:
	rm -f Net.txt ${DEFS} dumphstrerrno
