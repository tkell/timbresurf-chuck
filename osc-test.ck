

// There's a way to do file reads, it's in my email...


// construct the patch
SndBuf buf => Gain g => dac;
// set the gain
.5 => g.gain;

[ "/bar_0.wav", "/bar_1.wav", "/bar_2.wav", "/bar_3.wav"] @=> string paths[];

// Set up OSC
OscRecv recv;
// use port 12345
12345 => recv.port;
// start listening (launch thread)
recv.listen();

// create an address in the receiver, store in new variable
// WILL NEED to tweak this to get a 12-vector thing of floats each time 
recv.event( "/mouse/position, i" ) @=> OscEvent oe;

// OSC test!
while (true) {
    if (oe.nextMsg() != 0) {
        <<< oe.getInt() >>>; // eww, these prints.
        me.sourceDir() + paths[0] => buf.read;  
        buf.length() => now;
    }
}

