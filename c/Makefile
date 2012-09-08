all: lindev BlackBox

BlackBox: BlackBox.c openbsd.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E

lindev: BlackBox1.c openbsd.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBB0

clean:
	rm -f lindev BlackBox
