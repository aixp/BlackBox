# This is BSD Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

CFLAGS += -Wall -O0 -g

all: dev0 BlackBox

# -pthread required to dlopen libraries that depends on pthread

#BlackBox: BlackBox.c
#	${CC} ${CFLAGS} -o ${.TARGET} ${.ALLSRC} -L. -lBB -pthread

BlackBox: BlackBox-dl.c
	${CC} ${CFLAGS} -o ${.TARGET} ${.ALLSRC} -pthread

#dev0: BlackBox1.c
#	${CC} ${CFLAGS} -o ${.TARGET} ${.ALLSRC} -L . -lBB0

dev0: dev0.c
	${CC} ${CFLAGS} -o ${.TARGET} ${.ALLSRC}

clean:
	rm -f dev0 BlackBox
