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

	### encoder

	r.sort(key=lambda x: x[1])
	encS = []
	rs = 0
	checkDBCS = False
	for i, x in r:

		# i: encoding char in big-endian
		# x: ucs-2
		nb = nBytes(i)
		if nb > 1:
			checkDBCS = True

		if rs == 0:
			rs = 1
			rsi = i
			rsnb = nb
			rsx = x
			rsn = 0
		elif rs == 1:
			# nb == rsnb condition is redundant
			if (nb == rsnb) and (i == rsi + rsn + 1) and (x == rsx + rsn + 1):
				rsn = rsn + 1
			else:
				if rsn == 0:
					encS.append("\t\t\t| %s: y := %s" % (EC(rsx, "H"), EC(rsi, "H")))
				elif rsi == rsx:
					encS.append("\t\t\t| %s..%s: y := x" % (EC(rsx, "H"), EC(rsx + rsn, "H")))
				elif rsi > rsx:
					encS.append("\t\t\t| %s..%s: y := x + %s" % (EC(rsx, "H"), EC(rsx + rsn, "H"), EC(rsi - rsx, "H")))
				else: # rsi < rsx
					encS.append("\t\t\t| %s..%s: y := x - %s" % (EC(rsx, "H"), EC(rsx + rsn, "H"), EC(rsx - rsi, "H")))

				rsi = i
				rsnb = nb
				rsx = x
				rsn = 0
		else:
			assert False
	if rs == 1:
		if rsn == 0:
			encS.append("\t\t\t| %s: y := %s" % (EC(rsx, "H"), EC(rsi, "H")))
		elif rsi == rsx:
			encS.append("\t\t\t| %s..%s: y := x" % (EC(rsx, "H"), EC(rsx + rsn, "H")))
		elif rsi > rsx:
			encS.append("\t\t\t| %s..%s: y := x + %s" % (EC(rsx, "H"), EC(rsx + rsn, "H"), EC(rsi - rsx, "H")))
		else: # rsi < rsx
			encS.append("\t\t\t| %s..%s: y := x - %s" % (EC(rsx, "H"), EC(rsx + rsn, "H"), EC(rsx - rsi, "H")))

	if checkDBCS:
		s1 = """IF y < 256 THEN
				t[tW] := SHORT(CHR(y)); INC(tW)
			ELSE
				t[tW] := SHORT(CHR(y DIV 100H)); t[tW+1] := SHORT(CHR(y MOD 100H)); INC(tW, 2)
			END;"""
	else:
		s1 = """t[tW] := SHORT(CHR(y)); INC(tW);"""

	### decoder

	r.sort(key=lambda x: x[0])
	decS = []
	rs = 0
	if checkDBCS:
		decS.append('\t\t\tCASE d.st OF 0:')
		decS.append('\t\t\t\tCASE x OF')

		for i, x in r:
			# i: encoding char in big-endian
			# x: ucs-2
			if nBytes(i) == 1:
				if rs == 0:
					rs = 1
					rsi = i
					rsx = x
					rsn = 0
				elif rs == 1:
					if (i == rsi + rsn + 1) and (x == rsx + rsn + 1):
						rsn = rsn + 1
					else:
						if rsn == 0:
							decS.append("\t\t\t\t| %s: t[tW] := %s; INC(tW)" % (EC(rsi, "H"), EC(rsx, "X")))
						elif rsi == rsx:
							decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
						elif rsx > rsi:
							decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x + %s); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
						else: # rsx < rsi
							decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x - %s); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

						rsi = i
						rsx = x
						rsn = 0
				else:
					assert False
			else:
				break
		if rs == 1:
			if rsn == 0:
				decS.append("\t\t\t\t| %s: t[tW] := %s; INC(tW)" % (EC(rsi, "H"), EC(rsx, "X")))
			elif rsi == rsx:
				decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
			elif rsx > rsi:
				decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x + %s); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
			else: # rsx < rsi
				decS.append("\t\t\t\t| %s..%s: t[tW] := CHR(x - %s); INC(tW)" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

		i0 = set()
		for i, x in r:
			if nBytes(i) == 2:
				i0.add(i / 256)
		i0 = list(i0)
		i0.sort()
		decS.append("\t\t\t\t| %s: d.b := 256 * x; INC(d.st)" % (','.join([ EC(i, "H") for i in i0 ])))

		decS.append('\t\t\t\tELSE d.st := -1; RETURN END')
		decS.append('\t\t\t| 1:')
		decS.append('\t\t\t\tCASE x + d.b OF')

		rs = 0
		for i, x in r:
			if nBytes(i) == 2:
				if rs == 0:
					rs = 1
					rsi = i
					rsx = x
					rsn = 0
				elif rs == 1:
					if (i == rsi + rsn + 1) and (x == rsx + rsn + 1):
						rsn = rsn + 1
					else:
						if rsn == 0:
							decS.append("\t\t\t\t| %s: y := %s" % (EC(rsi, "H"), EC(rsx, "H")))
						elif rsi == rsx:
							decS.append("\t\t\t\t| %s..%s: y := x" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
						elif rsx > rsi:
							decS.append("\t\t\t\t| %s..%s: y := x + %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
						else: # rsx < rsi
							decS.append("\t\t\t\t| %s..%s: y := x - %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

						rsi = i
						rsx = x
						rsn = 0
				else:
					assert False
		if rs == 1:
			if rsn == 0:
				decS.append("\t\t\t\t| %s: y := %s" % (EC(rsi, "H"), EC(rsx, "H")))
			elif rsi == rsx:
				decS.append("\t\t\t\t| %s..%s: y := x" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
			elif rsx > rsi:
				decS.append("\t\t\t\t| %s..%s: y := x + %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
			else: # rsx < rsi
				decS.append("\t\t\t\t| %s..%s: y := x - %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

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
	else: # SBCS
		decS.append('\t\t\tCASE x OF')
		for i, x in r:
			if rs == 0:
				rs = 1
				rsi = i
				rsx = x
				rsn = 0
			elif rs == 1:
				if (i == rsi + rsn + 1) and (x == rsx + rsn + 1):
					rsn = rsn + 1
				else:
					if rsn == 0:
						decS.append("\t\t\t| %s: y := %s" % (EC(rsi, "H"), EC(rsx, "H")))
					elif rsi == rsx:
						decS.append("\t\t\t| %s..%s: y := x" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
					elif rsx > rsi:
						decS.append("\t\t\t| %s..%s: y := x + %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
					else: # rsx < rsi
						decS.append("\t\t\t| %s..%s: y := x - %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

					rsi = i
					rsx = x
					rsn = 0
			else:
				assert False
		if rs == 1:
			if rsn == 0:
				decS.append("\t\t\t| %s: y := %s" % (EC(rsi, "H"), EC(rsx, "H")))
			elif rsi == rsx:
				decS.append("\t\t\t| %s..%s: y := x" % (EC(rsi, "H"), EC(rsi + rsn, "H")))
			elif rsx > rsi:
				decS.append("\t\t\t| %s..%s: y := x + %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsx - rsi, "H")))
			else: # rsx < rsi
				decS.append("\t\t\t| %s..%s: y := x - %s" % (EC(rsi, "H"), EC(rsi + rsn, "H"), EC(rsi - rsx, "H")))

		decS.append('\t\t\tELSE\n\t\t\t\tRETURN\n\t\t\tEND;')
		decS.append('\t\t\tt[tW] := CHR(y); INC(tW);')

		s0 = " "
		s2 = "\t\tstate := FALSE"
		s3 = ", EMPTY"
		s4 = ""

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
