#! /usr/bin/env python2.7
#
# get map from Python codec

# return values:
#	r, e tables:
#		r: [ eord, uord ] table
#		e: list of warnings
def getMap (enc, tip):
	if tip == 'SBCS':
		N = 256
	elif tip == 'DBCS':
		N = 65536
	else:
		assert False

	e = []
	r = []
	i = 0
	while i < N:
		try:
			if i < 256:
				x = chr(i).decode(enc).encode('utf-16le')
			else:
				x = (chr(i / 256) + chr(i % 256)).decode(enc).encode('utf-16le')
		except UnicodeDecodeError:
			# e.append( '\t\t\tcan not decode CHR(%d)=0%02XX from %s encoding' % (i, i, enc) )
			pass
		else:
			if len(x) == 2:
				x = ord(x[0]) + 256 * ord(x[1])
				r.append( (i, x) )
			else:
				e.append( '\t\t\tcan not encode CHR(%d)=0%02XX from %s encoding to UCS-2' % (i, i, enc) )
		i = i + 1
	return r, e
