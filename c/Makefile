all: libdlobsdwrap.so lindev BlackBox

# libdlobsdwrap.so: universal method of correct access to dl* functions
#	in case of dynamic loading of libBB*.so "ld.so" in LibDl may be used instead of "libc.so", but not in case of static linking
#	wrapper method is universal

# -pthread required to dlopen libraries that depends on pthread
BlackBox: BlackBox.c
	${CC} ${CFLAGS} -Wall -O0 -g -o ${.TARGET} ${.ALLSRC} -L. -lBB -Wl,-E -pthread -ldlobsdwrap

lindev: BlackBox1.c
	${CC} ${CFLAGS} -Wall -O0 -g -o ${.TARGET} ${.ALLSRC} -L . -lBB0 -ldlobsdwrap

libdlobsdwrap.so: libdlobsdwrap.c
	${CC} ${CFLAGS} -Wall -O0 -g -o ${.TARGET} ${.ALLSRC} -fPIC -shared

clean:
	rm -f lindev BlackBox libdlobsdwrap.so
