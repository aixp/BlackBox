# This is GNU Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: dev0 BlackBox

CFLAGS += -Wall -O0 -g -m32

#BlackBox: BlackBox.c
#	${CC} ${CFLAGS} -o $@ $^ -L. -lBB

BlackBox: BlackBox-dl.c
	${CC} ${CFLAGS} -o $@ $^ -ldl

dev0: BlackBox1.c
	${CC} ${CFLAGS} -o $@ $^ -L . -lBB0

clean:
	rm -f dev0 BlackBox
