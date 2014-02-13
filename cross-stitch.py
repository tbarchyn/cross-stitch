#!/usr/bin/env python

import sys
import argparse
import scipy.ndimage
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt


## Process input arguments #####################################################
program_description = \
        '''Downsamples and modifies an image in order to create a pattern for
        cross stitching.'''
parser = argparse.ArgumentParser(description = program_description)
parser.add_argument('--infile', '-i', metavar='FILENAME', type=str, nargs=1,
        required=True, help='input image to process')
parser.add_argument('--outfile', '-o', metavar='FILENAME', type=str, nargs=1,
        required=True, help='save processed image as FILENAME')
parser.add_argument('--width', '-w', type=int, nargs=1, default=20,
        help='canvas width, default value = 20')
#parser.add_argument('--n-colors', '-c', type=int, nargs=1, default=10,
        #help='number of colors in output image, default value = 10')
args = parser.parse_args()
infile = args.infile[0]
outfile = args.outfile[0]
width = args.width

## Read image ##################################################################
try:
    im = scipy.ndimage.imread(infile)
except IOError:
    sys.stderr.write('could not open input file "' + infile + '"\n')
    sys.exit(1)

## Downsampling ################################################################
hw_ratio = float(im.shape[0])/im.shape[1]
new_size = (int(round(hw_ratio*width)), width)
im_small = scipy.misc.imresize(im, new_size)

## Process image colors ########################################################


## Generate output plot ########################################################
fig = plt.figure()
imgplot = plt.imshow(im_small)
imgplot.set_interpolation('nearest')
plt.grid()
plt.savefig(outfile)
