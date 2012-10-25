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

def main():
    f = open("a.save", 'r')
    audiofile = pickle.load(f)
    f.close()

    bars = audiofile.analysis.bars

    bar_counter = 0
    
    for bar in bars:
        output_filename = "bar_%s" % bar_counter
        bar_counter = bar_counter + 1

        collect = audio.AudioQuantumList()
        collect.append(bar)
        out = audio.getpieces(audiofile, collect)
        out.encode(output_filename)
        
        if bar_counter > 3:
            break


if __name__ == '__main__':
    import sys
    main()
