#! /usr/bin/env python2.7

SUBSYS = 'Enc'
MAPPREFIX = 'StdMap_'
OUTDIR = 'out'

import sys, os, string

import gen1, mapA, mappy, util

def isSDBCS (r):
	for eord, uord in r:
		if eord >= 65536:
			return False
	return True

def loadMap (format, db):
	if format == 'A':
		fh = open(db, 'rb')
		x = mapA.getMap(fh)
		fh.close()
	elif format == 'pySBCS':
		x = mappy.getMap(db, 'SBCS')
	elif format == 'pyDBCS':
		x = mappy.getMap(db, 'DBCS')
	else:
		assert False
	return x

def main ():
	done = {}
	while True:
		line = sys.stdin.readline()
		if line == '':
			break

		line = line.strip()
		if (len(line) > 0) and (line[0] != '#'):
			# print line
			enc, format, db, refComment = line.split(':	')
			enc = enc.strip()
			format = format.strip()
			db = db.strip()
			refComment = refComment.strip()

			assert not done.has_key(enc)
			done[enc] = True

			x = loadMap(format, db)

			if type(x) is not str:
				r, e = x
				assert len(r) > 0
				assert isSDBCS(r) # not implemented

				x = util.normEnc(enc)

				fName = os.path.join(OUTDIR, MAPPREFIX + x + '.txt')
				modName = SUBSYS + MAPPREFIX + x

				head0 = "Source: %s" % (refComment,)
				mod = gen1.gen(modName, r, e, head0=head0)

				fh = open(fName, 'wb')
				fh.write(mod)
				fh.close()
			else:
				print 'can not process %s %s %s: %s' % (enc, format, db, x)

if __name__ == '__main__':
	main()
