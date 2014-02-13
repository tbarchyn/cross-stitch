#!/usr/bin/env python

#import os, sys, getopt, Image
import argparse

#import numpy as np
#import matplotlib.pyplot as plt

class image:
    def __init__(self, in_file_path):
        pass

program_description = \
        '''Downsamples and modifies an image in order to create a pattern for
        cross stitching.'''
parser = argparse.ArgumentParser(description = program_description)
parser.add_argument('--infile', '-i', metavar='FILENAME', type=str, nargs=1,
        required=True, help='input image to process')
parser.add_argument('--outfile', '-o', metavar='FILENAME', type=str, nargs=1,
        required=True, help='save processed image as FILENAME')
parser.add_argument('--dpi', '-r', type=int, nargs=1, default=5,
        help='output file resolution (dots per inch), default value = 5')
args = parser.parse_args()
infile = args.infile[0]
outfile = args.outfile[0]
resolution = args.dpi
print infile
print outfile
print resolution
