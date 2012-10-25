#! /usr/bin/env python2.7
#
# Alexander Shiryaev, 2012.10
#
# MAPPINGS .TXT format A parser

import re

_p1 = re.compile("(0x[0-9a-fA-F]+)\s+(0x[0-9a-fA-F]+)\s+#")
_p2 = re.compile("0x[0-9a-fA-F]+\s*#\s*(UNDEFINED|DBCS LEAD BYTE)")

# return values:
#	r, e tables:
#		r: [ eord, uord ] table
#		e: list of warnings
#	| error string
def getMap (fh):
	e = []
	r = []
	de = {}
	du = {}
	while True:
		line = fh.readline()
		if line == '':
			break
		line = line.strip()
		if (len(line) > 0) and (line[0] != '#') and (line != chr(0x1a)):
			rr = _p1.match(line)
			if rr:
				eord = int(rr.group(1), 16)

				if len(rr.group(1)) == 4:
					assert eord < 256
				elif len(rr.group(1)) == 6:
					assert eord >= 256
				elif len(rr.group(1)) == 8:
					assert eord >= 65536
				else:
					print line
					assert False

				uord = int(rr.group(2), 16)

				assert uord < 65536

				# check unique eord
				if de.has_key(eord):
					# print line
					# print eord, de[eord]
					# assert False
					return "eord not unique"
				de[eord] = uord

				# check unique uord
				if du.has_key(uord):
					# print line
					# print du[uord], uord
					# assert False
					return "uord not unique"
				du[uord] = eord

				r.append( (eord, uord) )
			else:
				rr = _p2.match(line)
				if rr:
					pass # skip
				else:
					print line
					return "unexpected line"
	return r, e
