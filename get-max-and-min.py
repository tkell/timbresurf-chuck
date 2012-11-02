#!/usr/bin/env python
# encoding: utf=8
"""
This gets me the maxs and mins.
I will then hard-code them into oFX, because I am tacky like that
"""
import math

def main(inputFiles):
    maxes = [0, 0, 0, 0, 0, 0]
    mins = [0, 0, 0, 0, 0, 0]

    for inputFile in inputFiles:
        theFile = open(inputFile, 'r')
        index = 0
        for line in theFile:
            data = math.floor(float(line.strip()))
            if data > maxes[index]:
                maxes[index] = data
            if data < mins[index]:
                mins[index] = data
            index = (index + 1) % 6
    
    print "maximums:  %s" % maxes
    print "minimums:  %s" % mins

if __name__ == '__main__':
    import sys
    try:
        inputFiles = sys.argv[1:]
    except :
        print "Needs one or more input files, please"
        sys.exit(-1)
    main(inputFiles)
