// I think that the fileread code I need is in here:  "in.readline"
// https://ccrma.stanford.edu/courses/220a/homework/1/m220a-DataReader.ck

// We may have to hard-code the timbre data. bleeeeeeeeeeeh. 
[0.4, 0.6, 0.5, 0.65] @=> float timbre_1[];
[0.4, 0.6, 0.9, 0.75] @=> float timbre_2[];
[0.4, 0.6, 0.5, 0.85] @=> float timbre_3[];
[0.4, 0.6, 0.5, 0.65] @=> float timbre_4[];
[timbre_1, timbre_2, timbre_3, timbre_3] @=> float masterTimbre[][];


// construct the output patch
SndBuf buf => Gain g => dac;
// set the starting gain
.5 => g.gain;

[ "/bar_0.wav", "/bar_1.wav", "/bar_2.wav", "/bar_3.wav"] @=> string paths[];


// Set up OSC
OscRecv recv;
// use port 12345
12345 => recv.port;
// start listening (launch thread)
recv.listen();

// Create an address in the receiver, store in new variable
// Chuck seems to only like one point of data per variable
// Yeah, we'll eventually need 6 of these.
recv.event( "/mouse/position/x, i" ) @=> OscEvent recX;
recv.event( "/mouse/position/y, i" ) @=> OscEvent recY;


[0.4, 0.6, 0.5, 0.65] @=> float currentTimbre[];
for( 0 => int index; index < 4 ; index++ )
{
    // grab the latest OSC events
    if (recX.nextMsg() != 0) {
        <<< recX.getInt() >>>; // god, these debug prints are terrible
    }
    if (recY.nextMsg() != 0) {
        <<< recY.getInt() >>>; // god, these debug prints are STILL terrible
    }

    // If our conditional deals with gain, I think our life gets much easier..
    // This also means that as we move away from things, we can get louder or softer, if we're doing the 'hunt the timbre' game
    if (masterTimbre[index][2] > 0.7 && masterTimbre[index][3] > 0.7) {   
        0.0 => g.gain;
    }
    else {
        0.5 => g.gain;
    }

    me.sourceDir() + paths[index] => buf.read;  
    buf.length() => now;
}

