#!/usr/bin/env python
# encoding: utf=8
"""
This gets me the maxs and mins.
I will then hard-code them into oFX, because I am tacky like that
"""


def main(inputFiles):
    maxes = [0, 0, 0, 0, 0, 0]
    mins = [0, 0, 0, 0, 0, 0]

    for inputFile in inputFiles:
        theFile = open(inputFile, 'r')
        for line in theFile:
            theList = eval(line.strip()) # hahahahaha
            for index, timbre in enumerate(theList):
                if timbre > maxes[index]:
                    maxes[index] = timbre
                if timbre < mins[index]:
                    mins[index] = timbre
    
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
