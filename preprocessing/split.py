#!/usr/bin/python

''' 
Splits a file into two randomly, line by line.
Usage: split.py -h'

BASED ON: https://github.com/zygmuntz/phraug2/blob/master/split.py and http://fastml.com/processing-large-files-line-by-line/
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
'''


import argparse
import sys
import random
import time
import os

parser = argparse.ArgumentParser( description = "Split a file into two randomly, line by line." )
parser.add_argument( "input_file", help = "path to an input file" )
parser.add_argument( "output_file1", help = "path to the first output file (automatically appends extension of input file)" )
parser.add_argument( "output_file2", help = "path to the second output file (automatically appends extension of input file)" )
parser.add_argument( "-p", "--probability", help = "probability of writing to the first file (default 0.9)",
    default = 0.9, type = float )
parser.add_argument( "-r", "--random_seed", help = "random seed", default = False )
parser.add_argument( "-s", "--skip_headers", help = "skip the header line", 
    default = False, action = 'store_true' )
parser.add_argument( "-c", "--copy_headers", help = "copy the header line to both output files", 
    default = False, action = 'store_true' )

args = parser.parse_args()

seed = ""
if args.random_seed:
    random.seed( args.random_seed )
    seed = "_seed={0}".format(args.random_seed)

today = time.strftime("%Y%m%d")
test_probability = (100-float(args.probability)*100)/100.0
i_ext = os.path.splitext( args.input_file )[1]
o1_dir = os.path.split( args.output_file1 )[0]
o1_filename =  os.path.split( args.output_file1 )[1]
o2_dir = os.path.split( args.output_file2 )[0]
o2_filename =  os.path.split( args.output_file2 )[1]
o1_file = "{0}/{1}_{2}{3}{4}{5}".format(o1_dir, today, os.path.splitext( o1_filename )[0], args.probability, seed, i_ext )
o2_file = "{0}/{1}_{2}{3}{4}{5}".format(o2_dir, today, os.path.splitext( o2_filename )[0], test_probability, seed, i_ext )

with open( args.input_file ) as i:
    with open( o1_file, 'wb' ) as o1:
        with open( o2_file, 'wb' ) as o2:
            if args.skip_headers and args.copy_headers:
                print "You can either skip or copy headers, not both."
                quit()
            elif args.skip_headers:
                i.readline()
            elif args.copy_headers:
                headers = i.readline()
                o1.write( headers )
                o2.write( headers )

            counter = 0
            o1_count = 0
            for line in i:
                r = random.random()
                if r > args.probability:
                    o2.write( line )
                else:
                    o1.write( line )
                    o1_count += 1

                counter += 1
                if counter % 100000 == 0:
                    print counter

train_percentage = float(o1_count)/counter
print "Wrote {0}/{1}={2} of total number of lines to {3}".format(o1_count, counter, round(train_percentage,2), o1_file)
