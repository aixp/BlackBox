#! /usr/bin/env python2.7

def normEnc (enc):
	r = []
	for c in enc:
		o = ord(c)
		if (o >= ord('a')) and (o <= ord('z')):
			r.append(c)
		elif (o >= ord('A')) and (o <= ord('Z')):
			r.append(chr(o + ord('a') - ord('A')))
		elif (o >= ord('0')) and (o <= ord('9')):
			r.append(c)
		elif c == '-':
			r.append('_')
		else:
			assert False
	return ''.join(r)
