#!/usr/bin/python

""" 
Sample lines from input file with probability P, save them to output file'
Usage: sample_lines.py INPUT_FILE OUTPUT_FILE [P]

BASED ON: https://github.com/zygmuntz/phraug2/blob/master/sample.py
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

import csv
import sys
import random

try:
    P = float( sys.argv[3] )
except IndexError:
    P = 0.5
    
print "P = %s" % ( P )

input_file = sys.argv[1]
output_file = sys.argv[2]

i = open( input_file )
o = open( output_file, 'w' )

reader = csv.reader( i )
writer = csv.writer( o )

headers = reader.next()
writer.writerow( headers )

for line in reader:
    r = random.random()
    if r > P:
        continue

    writer.writerow( line )
