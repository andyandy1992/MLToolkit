#!/usr/bin/python

""" 
Standardises (shift and scale to zero mean and unit standard deviation) data from csv file.
(meant to be used together with col_stats.py)
Usage: standardise_features.py STATS_FILE INPUT_FILE OUTPUT_FILE [LABEL_INDEX]

BASED ON: https://github.com/zygmuntz/phraug2/blob/master/standardize.py
Copyright (c) 2013 Zygmunt Zajac
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys, csv
import numpy as np
from helpers.f_is_headers import *

stats_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

try:
    label_index = int( sys.argv[4] )
except IndexError:
    label_index = False
    
i = open( input_file )  
stats_reader = csv.reader( open( stats_file ))  
reader = csv.reader( i )
writer = csv.writer( open( output_file, 'wb' ))

# get stats

means = stats_reader.next()
means = np.array( map( float, means ))

standard_deviations = stats_reader.next()
standard_deviations = np.array( map( float, standard_deviations ))

# check headers

first_line = reader.next()
if is_headers( first_line ):
    headers = first_line
else:
    headers = False
    i.seek( 0 )
    
# go

for line in reader:
    
    if not label_index is False:
        l = line.pop( label_index ) 
        print l
        
    x = np.array( map( float, line ))
    
    # shift and scale
    x = x - means
    x = x / standard_deviations
    
    if not label_index is False:
        # -1.0,...
        #x = np.insert( x, 0, l )
        line = list( x )
        line.insert( 0, l )
    
    writer.writerow( line )
