#!/usr/bin/python
import os
import sqlite3
import pickle
import sys
import argparse

sys.path.append('/app/linux64')
from baf_reader import *
parser = argparse.ArgumentParser(description='Pickle Bruker X-MS data')
parser.add_argument('extraction', metavar='type', type=str,
                    help='Summary (meta) vs extraction of spectral data (edata)')
parser.add_argument('directory', type=str,
                    help='Path to Bruker directory (.s)')
parser.add_argument('-l', '--mslevel', default = 0, nargs='+',
                    help='MS level (default: 0)')
parser.add_argument('-sm', '--smode', default = 0, nargs='+',
                    help='Scan mode (default: 0)')
parser.add_argument('-am', '--amode', type=int, default = 2,
                    help='Acquisition mode (default: 2)')
parser.add_argument('-s', '--segment', default = 3, nargs='+',
                    help='Acquisition segment (default: 3)')

args = parser.parse_args()

if (args.extraction != 'meta') & (args.extraction != 'edata'):
    raise ValueError('Specify extraction type')

print(f'Extracting: {args.directory}', end='... ')
Exp1(fname=args.directory, type=args.extraction, mslevel=args.mslevel, smode=args.smode, amode=args.amode, seg=args.segment)
print('done')