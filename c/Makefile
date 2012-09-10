all: lindev BlackBox libdlobsdwrap.so

BlackBox: BlackBox.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E -pthread

lindev: BlackBox1.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBB0

libdlobsdwrap.so: libdlobsdwrap.c
	${CC} ${CFLAGS} -O0 -g -o ${.TARGET} ${.ALLSRC} -fPIC -shared

clean:
	rm -f lindev BlackBox libdlobsdwrap.so
