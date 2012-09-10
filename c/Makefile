all: libdlobsdwrap.so lindev BlackBox

BlackBox: BlackBox.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E -pthread -ldlobsdwrap

lindev: BlackBox1.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBB0 -ldlobsdwrap

libdlobsdwrap.so: libdlobsdwrap.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -fPIC -shared

clean:
	rm -f lindev BlackBox libdlobsdwrap.so
