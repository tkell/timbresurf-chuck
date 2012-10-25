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
        output_filename = "%s_%s" % (granularity, counter)
        counter = counter + 1
        
        # Commented out for speed while I test the file-writing
#        collect = audio.AudioQuantumList()
#        collect.append(chunk)
#        out = audio.getpieces(audiofile, collect)
#        out.encode(output_filename)

        # now I need to write things
        # I am going to take timbre values 1 through 7, as 0 is just amplitude.
        if granularity == "segment":
            temp_timbre =  chunk.timbre[1:7]

        # Work out how to get averages here
        # There must be a better way to get segments from an audioQuanta...
        temp_timbre = []
        if granularity != "segment":
            for segment in all_segments:
                if segment.start >= chunk.start and segment.start < chunk.get_end():
                    temp_timbre.append(segment.timbre[1:7])
                elif segment.start > chunk.get_end():
                    break
        temp_timbre = numpy.array(temp_timbre)
        timbre_list = list(temp_timbre.mean(axis=0))
        timbre_list = [math.floor(t) for t in timbre_list]
        f.write("%s\n" % list(timbre_list))
        

        # debugz to stop things
        if counter >= 1:
            break
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
    
