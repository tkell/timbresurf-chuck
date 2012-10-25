#!/usr/bin/env python
# encoding: utf=8
"""
test.py

Simple test script for testing echonest remix.
Outputs the first and second beat of each bar.  

By Thor Kell, 2012-08-14.  (with huge thanks to Ben Lacker)
"""

usage = """
Usage: 
    python test.py <input_filename> <output_filename>

Example:
    python test.py EverythingIs.mp3 EverythingIsOneandTwo.mp3
"""

import echonest.audio as audio
import pickle

def main(input_filename):
    
    #audiofile = audio.LocalAudioFile(input_filename)
    #f = open("a.save", 'w')
    #pickle.dump(audiofile, f)
    #f.close()

    f = open("a.save", 'r')
    audiofile = pickle.load(f)
    f.close()

    segments = audiofile.analysis.segments
    collect = audio.AudioQuantumList()
    for segment in segments:
        collect.append(segment)
    out = audio.getpieces(audiofile, collect)
    out.encode(output_filename)


if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(input_filename)
