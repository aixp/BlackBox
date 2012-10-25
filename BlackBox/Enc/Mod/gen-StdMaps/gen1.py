#! /usr/bin/env python2.7
#
# A. V. Shiryaev, 2012.10
#
# generate encoder/decoder UCS-2 <-> SBCS/DBCS-encoding for Component Pascal

import sys

def be2le (x):
	y = 0
	while x > 0:
		y = y * 256 + x % 256
		x = x / 256
	return y

def nBytes (x):
	if x == 0:
		return 1
	else:
		y = 0
		while x > 0:
			y = y + 1
			x = x / 256
		return y

def EC (x, p="X"):
	if x < 0:
		x = -x
		s = '-'
	else:
		s = ''
	if x < 0xA0:
		return "%s%02X%s" % (s, x, p)
	elif x < 256:
		return "%s0%02X%s" % (s, x, p)
	elif x < 0xA000:
		return "%s%04X%s" % (s, x, p)
	else:
		return "%s0%04X%s" % (s, x, p)

def RC (x, p="X"):
	x = list(x) # copy
	x.sort()
	s = []
	st = 0
	for i in x:
		if st == 0:
			sti = i
			stn = 0
			st = 1
		elif st == 1:
			if i == sti + stn + 1:
				stn = stn + 1
			else:
				if stn == 0:
					s.append(EC(sti, p))
				elif stn == 1:
					s.append(EC(sti, p))
					s.append(EC(sti + 1, p))
				else:
					s.append("%s..%s" % (EC(sti, p), EC(sti + stn, p)))
				sti = i
				stn = 0
	if st == 1:
		if stn == 0:
			s.append(EC(sti, p))
		elif stn == 1:
			s.append(EC(sti, p))
			s.append(EC(sti + 1, p))
		else:
			s.append("%s..%s" % (EC(sti, p), EC(sti + stn, p)))
	return ','.join(s)

# for encoder
def opt0 (r):
	o = {}
	for i, x in r:
		ofs = i - x
		if o.has_key(ofs):
			o[ofs].append(x)
		else:
			o[ofs] = [ x ]
	return o

# for decoder
def opt1 (r, nb):
	o = {}
	for i, x in r:
		if nBytes(i) == nb:
			ofs = x - i
			if o.has_key(ofs):
				o[ofs].append(i)
			else:
				o[ofs] = [ i ]
	return o

def gen (modName, r, head, head0=None):
	e = head
	if len(e) > 0:
		if head0:
			head0S = '%s\n\n\t\t' % (head0,)
		else:
			head0S = ''
		errS = """
	(*
		%sErrors:
%s
	*)
""" % (head0S, '\n'.join(e),)
	else:
		if head0:
			errS = "\n\t(* %s *)\n" % (head0,)
		else:
			errS = ''

	### calc man num of SHORTCHARs per CHAR
	maxN = 1
	for i, x in r:
		# i: encoding char in big-endian
		# x: ucs-2
		nb = nBytes(i)
		if nb > maxN:
			maxN = nb

	### encoder

	r.sort(key=lambda x: x[1])
	encS = []

	o = opt0(r)
	for k, v in o.iteritems():
		if len(v) == 1:
			encS.append("\t\t\t| %s: y := %s" % (EC(v[0], "H"), EC(k + v[0], "H")))
		else:
			encS.append("\t\t\t| %s: y := %s + x" % (RC(v, "H"), EC(k, "H")))

	if maxN == 2: # DBCS
		s1 = """IF y < 256 THEN
				t[tW] := SHORT(CHR(y)); INC(tW)
			ELSE
				t[tW] := SHORT(CHR(y DIV 100H)); t[tW+1] := SHORT(CHR(y MOD 100H)); INC(tW, 2)
			END;"""
	elif maxN == 1: # SBCS
		s1 = """t[tW] := SHORT(CHR(y)); INC(tW);"""
	else:
		assert False # not implemented

	### decoder

	r.sort(key=lambda x: x[0])
	decS = []
	rs = 0
	if maxN == 2: # DBCS
		decS.append('\t\t\tCASE d.st OF 0:')
		decS.append('\t\t\t\tCASE x OF')

		o = opt1(r, 1)
		for k, v in o.iteritems():
			if len(v) == 1:
				decS.append("\t\t\t\t| %s: t[tW] := %s; INC(tW)" % (EC(v[0], "H"), EC(k + v[0], "X")))
			else:
				decS.append("\t\t\t\t| %s: t[tW] := CHR(%s + x); INC(tW)" % (RC(v, "H"), EC(k, "H")))

		i0 = set()
		for i, x in r:
			if nBytes(i) == 2:
				i0.add(i / 256)
		i0 = list(i0)
		i0.sort()
		decS.append("\t\t\t\t| %s: d.b := 256 * x; INC(d.st)" % (RC(i0, "H"),))

		decS.append('\t\t\t\tELSE d.st := -1; RETURN END')
		decS.append('\t\t\t| 1:')
		decS.append('\t\t\t\tCASE x + d.b OF')

		o = opt1(r, 2)
		for k, v in o.iteritems():
			if len(v) == 1:
				decS.append("\t\t\t\t| %s: y := %s" % (EC(v[0], "H"), EC(k + v[0], "H")))
			else:
				decS.append("\t\t\t\t| %s: y := %s + x" % (RC(v, "H"), EC(k, "H")))

		decS.append('\t\t\t\tELSE d.st := -1; RETURN END;')
		decS.append('\t\t\t\tt[tW] := CHR(y); INC(tW);')
		decS.append('\t\t\t\tDEC(d.st)')
		decS.append('\t\t\tEND;')

		s0 = """
			b: INTEGER;
			st: INTEGER; (* 0 - no state, > 0 - number of chars expected, -1 - error *)
		"""
		s2 = """\t\tIF d.st = 0 THEN state := FALSE
		ELSIF d.st > 0 THEN state := TRUE
		ELSE HALT(100)
		END"""
		s3 = """;
	BEGIN d.st := 0
	END Reset"""
		s4 = " d.Reset;"
	elif maxN == 1: # SBCS
		decS.append('\t\t\tCASE x OF')

		o = opt1(r, 1)
		for k, v in o.iteritems():
			if len(v) == 1:
				decS.append("\t\t\t| %s: y := %s" % (EC(v[0], "H"), EC(k + v[0], "H")))
			else:
				decS.append("\t\t\t| %s: y := %s + x" % (RC(v, "H"), EC(k, "H")))

		decS.append('\t\t\tELSE\n\t\t\t\tRETURN\n\t\t\tEND;')
		decS.append('\t\t\tt[tW] := CHR(y); INC(tW);')

		s0 = " "
		s2 = "\t\tstate := FALSE"
		s3 = ", EMPTY"
		s4 = ""
	else:
		assert False # not implemented

	return """MODULE %s;

	(* This file was generated automatically *)
%s
	IMPORT Codecs := EncCodecs;

	TYPE
		Encoder = POINTER TO RECORD (Codecs.Encoder) END;
		Decoder = POINTER TO RECORD (Codecs.Decoder)%sEND;

	(* Encoder *)

	PROCEDURE (e: Encoder) Encode (IN f: ARRAY OF CHAR; VAR fR, fLen: INTEGER; VAR t: ARRAY OF SHORTCHAR; VAR tW: INTEGER);
		VAR x, y: INTEGER;
	BEGIN
		WHILE fLen > 0 DO
			x := ORD(f[fR]);
			CASE x OF
%s
			ELSE
				RETURN
			END;
			%s
			INC(fR); DEC(fLen)
		END
	END Encode;

	PROCEDURE NewEncoder* (): Codecs.Encoder;
		VAR e: Encoder;
	BEGIN
		NEW(e); RETURN e
	END NewEncoder;

	(* Decoder *)

	PROCEDURE (d: Decoder) Decode (IN f: ARRAY OF SHORTCHAR; VAR fR, fLen: INTEGER; VAR t: ARRAY OF CHAR; VAR tW: INTEGER; OUT state: BOOLEAN);
		VAR x, y: INTEGER;
	BEGIN
		WHILE fLen > 0 DO
			x := ORD(f[fR]);
%s
			INC(fR); DEC(fLen)
		END;
%s
	END Decode;

	PROCEDURE (d: Decoder) Reset%s;

	PROCEDURE NewDecoder* (): Codecs.Decoder;
		VAR d: Decoder;
	BEGIN
		NEW(d);%s RETURN d
	END NewDecoder;

END %s.""" % (modName, errS, s0, '\n'.join(encS), s1, '\n'.join(decS), s2, s3, s4, modName)
