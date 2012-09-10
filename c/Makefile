all: lindev BlackBox

BlackBox: BlackBox.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E -pthread

lindev: BlackBox1.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBB0

clean:
	rm -f lindev BlackBox
