#include <sys/types.h>
#include <sys/signal.h>
#include <setjmp.h>
#include <stdlib.h>
#include <stdio.h>

#define TABS "\t\t"

static void D (const char *s, int sz, int set)
{
	int res;

	res = printf("%s%s* = ", TABS, s);
	if (sz == 1) {
		res = printf("SHORTCHAR");
	} else if (sz == 2) {
		res = printf("SHORTINT");
	} else if (sz == 4) {
		if (set) {
			res = printf("SET");
		} else {
			res = printf("INTEGER");
		}
	} else if (sz == 8) {
		if (set) {
			res = printf("ARRAY [untagged] 2 OF SET");
		} else {
			res = printf("LONGINT");
		}
	} else {
		res = printf("ARRAY [untagged] ");
		if (sz % 4 == 0) {
			if (set) {
				res = printf("%d OF SET", sz / 4);
			} else {
				res = printf("%d OF INTEGER", sz / 4);
			}
		} else {
			res = printf("%d OF SHORTCHAR", sz);
		}
	}
	res = printf(";\n");
}

int main ()
{
	D("PtrVoid", sizeof(void *), 0);
	D("int", sizeof(int), 0);
	D("long", sizeof(long), 0);
	D("ulong", sizeof(unsigned long), 0);
	D("size_t", sizeof(size_t), 0);
	D("ssize_t", sizeof(ssize_t), 0);
	D("off_t", sizeof(off_t), 0);
	D("clock_t", sizeof(clock_t), 0);
	D("time_t", sizeof(time_t), 0);
	D("mode_t", sizeof(mode_t), 1);
	D("pid_t", sizeof(pid_t), 0);
	D("uid_t", sizeof(uid_t), 0);
	D("gid_t", sizeof(gid_t), 0);
	D("dev_t", sizeof(dev_t), 0);
	D("ino_t", sizeof(ino_t), 0);
	D("nlink_t", sizeof(nlink_t), 0);
	D("int8_t", sizeof(int8_t), 0);
	D("u_int8_t", sizeof(u_int8_t), 0);
	D("int16_t", sizeof(int16_t), 0);
	D("u_int16_t", sizeof(u_int16_t), 0);
	D("int32_t", sizeof(int32_t), 0);
	D("u_int32_t", sizeof(u_int32_t), 0);
	D("int64_t", sizeof(int64_t), 0);
	D("u_int64_t", sizeof(u_int64_t), 0);
	D("wchar_t", sizeof(wchar_t), 0);
	D("sigset_t", sizeof(sigset_t), 1);
	D("sigjmp_buf", sizeof(sigjmp_buf), 0);
	D("intFlags", sizeof(int), 1);
	D("FILE", sizeof(FILE), 0);

	return 0;
}
