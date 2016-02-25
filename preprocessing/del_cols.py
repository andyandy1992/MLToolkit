#!/usr/bin/python

""" 
Delete columns from file specified by their indexes.
Usage: del_cols.py -h

BASED ON: https://github.com/zygmuntz/phraug2/blob/master/delete_cols.py
Copyright (c) 2013 Zygmunt Zajaoc
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
import argparse

parser = argparse.ArgumentParser(description='delete some columns from file, given by their indexes')
parser.add_argument("input_file", help = "path to csv input file")
parser.add_argument("output_file", help = "path to output file")
parser.add_argument('index', metavar='I', type=int, nargs='+',
                            help='an index or indexes to delete')
parser.add_argument("-v", "--verbose", help = "will write counts during process to standard out",
                    action = "store_true", default = False)

args = parser.parse_args()
args.index.sort( reverse = True )

if args.verbose:
    print "%s ---> %s" % ( args.input_file, args.output_file )
    print "header indices: %s" % ( args.index )

reader = csv.reader(open( args.input_file ))
writer = csv.writer(open( args.output_file, 'wb' ))

counter = 0
for line in reader:
    #deal with empty line
    if not line:
        break

    for h in args.index:
        del line[h]

    writer.writerow( line )

    counter += 1
    if counter % 10000 == 0 and args.verbose:
        print counter
