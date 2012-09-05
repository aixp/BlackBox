all: interp BlackBox

BlackBox: BlackBox.c openbsd.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E

interp: BlackBox1.c openbsd.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBBInterp

clean:
	rm -f interp BlackBox
