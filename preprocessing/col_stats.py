#!/usr/bin/python

""" 
Compute column means and standard deviations from data in csv file.
Usage: colstats.py -h

BASED ON: https://github.com/zygmuntz/phraug2/blob/master/colstats.py
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

"""
compute column means and standard deviations from data in csv file
"""

import sys, csv
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "input_file", help = "path to csv input file" )
parser.add_argument( "output_file", help = "path to output file" )
parser.add_argument( "--header", help = "Specify if file has header", 
    action="store_true", default = False )
parser.add_argument( "-l", "--label_index", help = "Specify label index",
    type = int, default = False )

args = parser.parse_args()


i = open( args.input_file )
reader = csv.reader( i )
writer = csv.writer( open( args.output_file, 'wb' ))

# check headers

if args.header:
    first_line = reader.next()

n = 0

for line in reader:
    n += 1

    #to handle empty lines at the end if file
    if not line:
        break

    if args.label_index:
        line.pop( args.label_index )

    x = np.array( map( float, line ))
    x2 = np.square( x )

    # First pass initialize np arrays
    if n == 1:
        sums_x = x
        sums_x2 = x2
    else:
        sums_x += x
        sums_x2 += x2


# preparation

print n
print sums_x
print sums_x2

means = sums_x / n
sums2_x = np.square( sums_x )

#print means
#print sums2_x

variances = sums_x2 / n - sums2_x / ( n ** 2 )
standard_deviations = np.sqrt( variances )

#print variances
#print standard_deviations

# save stats
if args.header:
   writer.writerow( first_line )

writer.writerow( means )
writer.writerow( standard_deviations )
