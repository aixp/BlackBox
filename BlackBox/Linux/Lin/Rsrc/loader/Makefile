# This is GNU Makefile
#    BSD       GNU
# ${.TARGET}    $@
# ${.ALLSRC}    $^
# ${.IMPSRC}    $<

all: lindev BlackBox BlackBox-dl

CFLAGS += -Wall -O0 -g -m32

BlackBox: BlackBox.c
	${CC} ${CFLAGS} -o $@ $^ -L. -lBB

BlackBox-dl: BlackBox-dl.c
	${CC} ${CFLAGS} -o $@ $^ -ldl

lindev: BlackBox1.c
	${CC} ${CFLAGS} -o $@ $^ -L . -lBB0

clean:
	rm -f lindev BlackBox BlackBox-dl
