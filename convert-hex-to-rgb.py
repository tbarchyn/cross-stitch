#!/usr/bin/env python
import numpy

_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in
    _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def rgb(triplet):
        return (_HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]],
                _HEXDEC[triplet[4:6]])

#hexlist = numpy.loadtxt('./256-color.dat')
rgblist = numpy.empty((256,3))
fin = open('./256-color.dat')
i = 0
for line in fin:
    #print line,
    rgbval = rgb(line)
    #print rgbval
    rgblist[i,:] = rgbval
    i += 1

numpy.savetxt('256-color-rgb.dat', rgblist, fmt='%d')
