#!/usr/bin/python
import os
import sqlite3
import pickle
import sys
import argparse

sys.path.append('/app/linux64')
from baf_reader import *


# bconvert

# if len(sys.argv) > 0:
#     print(str(sys.argv))
#     mslev = int(sys.argv[1])
#     if (mslev != 0) & (mslev != 1):
#         raise ValueError('MS level is 0 or 1')
# else:
#     mslev = 1


if len(sys.argv) > 0:
    print(str(sys.argv))
    extraction = sys.argv[1]
    if (extraction != 'meta') & (extraction != 'edata'):
        raise ValueError('Specify extraction type')
else:
    extraction = 'edata'



k=sys.argv[2]
print(f'Extracting: {k}', end='... ')
o = Exp(fname=k, type=extraction)
#pickle.dump([o.infile, o.properties, o.nSpectra, o.edata, o.outfile], open(o.outfile, "wb"))
print('done')


# k=os.listdir('/data/.')[3]
# listOfFiles = os.listdir('/data/.')
# print(f'{len(listOfFiles)} folders in dir')
# 
# for k in listOfFiles:
#     if '.d' in k:
#         print(f'STARTING: {k}')
#         try:
#             o = Exp(fname=k, type=extraction)
#         except:
#             print(f'Error reading')
#             continue
#         try:
#             pickle.dump([o.infile, o.properties, o.nSpectra, o.sdata, o.outfile], open(o.outfile, "wb"))
#             print('		done')
#         except:
#             print(f'Error pickle')
#     continue
