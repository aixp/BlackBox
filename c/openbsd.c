#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <setjmp.h>
#include <stdio.h>

#include <errno.h>

/*
int __sigsetjmp(sigjmp_buf env, int savemask)
{
	printf("__sigsetjmp ...\n");
	return sigsetjmp(env, savemask);
}
*/

int __xstat (int version, const char *path, struct stat *sb)
{
	if (version != 3) {
		printf("WARNING: __xstat: %d %s\n", version, path);
	}
	return stat(path, sb); /* XXX */
}

#undef stdin
void * stdin = (&__sF[0]);

#undef stdout
void * stdout = (&__sF[1]);

#undef stderr
void * stderr = (&__sF[2]);
