#!/usr/bin/env python

import sys
import argparse
import scipy.ndimage
import scipy.misc
import scipy.cluster
import numpy as np
import matplotlib.pyplot as plt


## Process input arguments #####################################################
program_description = \
        '''Downsamples and modifies an image in order to create a pattern for
        cross stitching.'''
parser = argparse.ArgumentParser(description = program_description)
parser.add_argument('--infile', '-i', metavar='file', type=str, nargs=1,
        required=True, help='input image to process')
parser.add_argument('--outfile', '-o', metavar='file', type=str, nargs=1,
        required=True, help='save processed image as file')
parser.add_argument('--width', '-w', type=int, nargs=1, default=20,
        help='canvas width, default value = 20')
parser.add_argument('--ncolors', '-c', type=int, nargs=1, default=16,
        help='number of colors in output image, default value = 16')
args = parser.parse_args()
infile = args.infile[0]
outfile = args.outfile[0]
width = args.width[0]
ncolors = args.ncolors

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
ar = im_small.reshape(scipy.product(im_small.shape[:2]), im_small.shape[2])
colors, dist = scipy.cluster.vq.kmeans(ar, ncolors)
c = ar.copy()
vecs, dist = scipy.cluster.vq.vq(ar, colors)
for i, color in enumerate(colors):
    c[scipy.r_[scipy.where(vecs==i)],:] = color
im_small_reduced = c.reshape(new_size[0], new_size[1], 3)

## Generate output plot ########################################################
fig = plt.figure()
imgplot = plt.imshow(im_small_reduced)
imgplot.set_interpolation('nearest')
plt.grid()
plt.savefig(outfile)
