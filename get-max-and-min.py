#!/usr/bin/env python
# encoding: utf=8
"""
This gets me the maxs and mins.
I will then hard-code them into oFX, because I am tacky like that
"""
import math
import os
def main():

    maxes = [0, 0, 0, 0, 0, 0]
    mins = [0, 0, 0, 0, 0, 0]
    inputFiles = []
    
    # Brittle:  can only be run from the dir it is in
    path = 'audio/'
    subdirs = os.listdir(path)

    # find all my files
    for subdir in subdirs:
        subdir_path = path + subdir + '/'
        all_files = os.listdir(path + subdir)
        for filename in all_files:
            if 'timbre' in filename:
                inputFiles.append(subdir_path + filename)
        
    # get the mins and maxes
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
    main()
