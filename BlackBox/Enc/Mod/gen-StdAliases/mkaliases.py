#! /usr/bin/env python2.7
#
# Alexander Shiryaev, 2012.10

import sys
import string

def loadMap (fh):
	r = {}
	fix = {}
	rfix = {}
	ident = 0
	while True:
		line = fh.readline()
		if line == '':
			break
		line = line.strip()
		if (len(line) > 0) and (line[0] != '#'):
			t, fs = string.split(line, ':', maxsplit=1)
			t = t.rstrip()
			fs = fs.lstrip()
			fs = fs.split()
			for f in fs:
				assert not r.has_key(f)
				x = fix.get(t)
				if x == None:
					x = ident
					ident = ident + 1
					fix[t] = x
					rfix[x] = t
				r[f] = x
	return r, rfix

def mkTree (m):
	r = {}
	for f, t in m.iteritems():
		n = r
		i = 0
		while i < len(f):
			c = f[i]
			n = n.setdefault(c, {})
			i = i + 1
		assert not n.has_key(0)
		n[0] = t
	return r

def gen0 (t,level, n):
	assert len(t) > 0

	r = []

	if len(t) == 1:
		if t.has_key(0):
			r.append('%sIF s[%d] = 0X THEN x := %d END' % ('\t'*n, level, t[0]))
		else:
			k = t.keys()[0]
			r.append("%sIF s[%d] = '%c' THEN" % ('\t'*n, level, k))
			r.append(gen0(t[k], level+1, n+1))
			r.append("%sEND" % ('\t'*n))
	else:
		r.append("%sCASE s[%d] OF" % ('\t'*n, level))
		for k, v in t.iteritems():
			if k != 0:
				r.append("%s| '%c':" % ('\t'*n, k))
				r.append(gen0(v, level+1, n+1))
			else:
				r.append('%s| 0X: x := %d' % ('\t'*n, v))
		r.append("%sELSE END" % ('\t'*n,))

	return '\n'.join(r)

def gen (t, rfix):
	fixS = []
	for k, v in rfix.iteritems():
		fixS.append('\t| %d: r := modPrefix + "%s"' % (k, string.replace(v.lower(), '-', '_')))

	return """MODULE EncStdAliases;

(* Generated automatically *)

CONST
	modPrefix = "EncStdMap_";

PROCEDURE GetModName* (s: ARRAY OF CHAR; OUT r: ARRAY OF CHAR; OUT ok: BOOLEAN);
	VAR x: INTEGER;
BEGIN
	x := 0;
	WHILE (x < LEN(s)) & (s[x] # 0X) DO
		IF (s[x] >= 'a') & (s[x] <= 'z') THEN
			s[x] := CHR(ORD(s[x]) - ORD('a') + ORD('A'))
		END;
		INC(x)
	END;

	x := -1;
%s;

	ok := TRUE;
	CASE x OF -1: ok := FALSE
%s
	END
END GetModName;

END EncStdAliases.""" % (gen0(t, 0, 1), '\n'.join(fixS))

def main ():
	m, rfix = loadMap(sys.stdin)
	sys.stdout.write(gen(mkTree(m), rfix))

if __name__ == '__main__':
	main()
