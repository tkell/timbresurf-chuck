#!/usr/bin/env python
# encoding: utf=8
"""
This chops things into segments, tatums, beats, or bars.  
It writes audio files of each of those, and writes .txt.en files with the corresponding timbre data

"""

usage = """
Usage: 
    python remix-split.py <segment|tatum|beat|bar> <input_filename>
Example:
    python remix-split.py EverythingIsGoingToBeOK.mp3 
"""

import os
import math
import numpy
import echonest.audio as audio

def main(input_filename):
    audiofile = audio.LocalAudioFile(input_filename)

    if granularity == "segment":
        all_audio = audiofile.analysis.segments
    elif granularity == "tatum":
        all_audio = audiofile.analysis.tatums
    elif granularity == "beat":
        all_audio = audiofile.analysis.beats
    elif granularity == "bar":
        all_audio = audiofile.analysis.bars

    all_segments = audiofile.analysis.segments

    output_text_filename = "%ss%s" % (granularity, ".timbre")
    f = open(output_text_filename, 'w')
    counter = 0
    for chunk in all_audio:
        output_filename = "%s_%s.wav" % (granularity, counter)
        counter = counter + 1
        
        collect = audio.AudioQuantumList()
        collect.append(chunk)
        out = audio.getpieces(audiofile, collect)
        out.encode(output_filename)     

        # Now I need to write things
        # I am going to take timbre values 1 through 7, as 0 is just amplitude.
        temp_timbre = []
        if granularity == "segment":
            temp_timbre = [chunk.timbre[1:7]] # This is needed to make things work with the numpy array stuff

        # Work out how to get averages here
        # There must be a better way to get segments from an audioQuanta...
        if granularity != "segment":
            for segment in all_segments:
                if segment.start >= chunk.start and segment.start < chunk.get_end():
                    temp_timbre.append(segment.timbre[1:7])
                elif segment.start > chunk.get_end():
                    break
            # This is if we have no segments that starts in the chunk
            if not temp_timbre:
                for segment in all_segments:
                    if segment.start < chunk.start and segment.end > chunk.get_end():
                        temp_timbre.append(segment.timbre[1:7])
                        break
        
        temp_timbre = numpy.array(temp_timbre)
        if temp_timbre.size == 0:
            temp_timbre = numpy.array([[0, 0, 0, 0, 0, 0]])
        timbre_list = list(temp_timbre.mean(axis=0))
        timbre_list = [str(math.floor(t)) for t in timbre_list]

        # Yes, I am writing one number per line.  Shhh.  ChucK's string reading abilities are awful
        for timbre in timbre_list:
            f.write("%s\n" % timbre) 
    
    f.close()

if __name__ == '__main__':
    import sys
    try:
        granularity = sys.argv[1]
        inputFilename = sys.argv[2]
    except :
        print usage
        sys.exit(-1)
    if not granularity in ['segment', 'tatum', 'beat', 'bar']:
        print usage
        sys.exit(-1)
    main(inputFilename)
    
