#!/usr/bin/env python

import sys
import argparse
import Image
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
args = parser.parse_args()
infile = args.infile[0]
outfile = args.outfile[0]
width = args.width

## Read image ##################################################################
try:
    im = Image.open(infile)
except IOError:
    sys.stderr.write('could not open input file "' + infile + '"\n')
    sys.exit(1)

## Downsampling ################################################################
hw_ratio = float(im.size[1])/im.size[0]
new_size = (width, int(round(hw_ratio*width)))
im = im.resize(new_size)

## Process image colors ########################################################


## Generate output plot ########################################################


