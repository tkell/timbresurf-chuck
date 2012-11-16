/*
God bless Ben Lacker for teaching me to write things well
This is the main file for running Timbre Hero. 
You give it a filename and a difficulty.
Run only AFTER turning the kinect on.  
*/

// USEAGE:  
"Useage:  chuck playback.ck:<filename>:<bar|beat|tatum|segment>" => string useage;

if (me.args() != 2) {
    <<< useage >>>;
    // i'd like to quit here, I sure would...
}

0 => float score;

// Globals that I can use in both 
int right_hand[3]; // the right hand controls dimensions 1, 2, 3
int left_hand[3]; // the right hand controls dimensions 4, 5, 6
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0] @=> float distances[];
0.0 => float the_distance;
0.0 => float gain_modifier;

// Concurrent OSC listener
fun void osc_shred() {
    OscRecv recv;
    12345 => recv.port;
    recv.listen();

    // Create an address in the receiver, store in new variable
    // Chuck seems to only like one point of data per variable
    // Yeah, we'll eventually need 6 of these.
    recv.event("/mouse/position, i, i") @=> OscEvent recX;

    // I'll need to fit everything into one message, I think...
    while (true) {
        recX => now;
        if (recX.nextMsg() != 0) {
            recX.getInt()=> right_hand[0];
            recX.getInt()=> right_hand[1];
            //<<< "from osc: ", right_hand[0]>>>;
            //<<< "from osc: ", right_hand[1]>>>;
        } 
    }
}

// Set up OSC sender
OscSend oscSender;
oscSender.setHost("localhost", 23456);


// construct the output patch
SndBuf buf => Gain g => dac;
// set the starting gain
.5 => g.gain;

// Set path, timbre fil[ename, and audio filename up based on input arguments
"/" => string path;
if (me.arg(0) == "test") {
    "audio/test/" => path;
}
me.arg(1) => string segment_type;
path + segment_type + "s.timbre" => string timbre_filename;
segment_type + "_" => string chunk_filename_base;


// How many chunks of audio do we have ?
0 => int file_length;
FileIO @ in;
new FileIO @=> in;
in.open(timbre_filename, FileIO.READ );
while (in.eof() != true) {
    in.readLine();
    file_length + 1 => file_length;
}
in.close();
(file_length - 1) / 6 => file_length;

// Open the timbre file for reading
// This is cryptic because splitting strings in chuck is lousy
// For the moment, we're actually going to make a flat array, and mod it by 6.  Eww
float timbre[file_length * 6];
0 => int timbre_counter;
in.open(timbre_filename, FileIO.READ );
while (in.eof() != true) {
    in.readLine() => string theLine; // read a line
    if (theLine != "") {
    Std.atof(theLine) => float timbre_value;
    timbre_value => timbre[timbre_counter];
    timbre_counter + 1 => timbre_counter;
    }
}
in.close();

// Start the OSC listener
spork ~ osc_shred();

// Begin the main loop!
0 => int timbre_index;
for( 0 => int index; index < file_length ; index++ ) {
    // At the top of each bar, I send a tick to the oFX visualizer
    oscSender.startMsg("visuals/tick");

    // Now I have to find the right timbre values
    index * 6 => timbre_index;
    Std.fabs(timbre[timbre_index] - right_hand[0]) => distances[0];
    Std.fabs(timbre[timbre_index + 1] - right_hand[1]) => distances[1];
    <<< "X distance:  ", distances[0] >>>;
    <<< "Y Distance:  ", distances[1] >>>;

    // Compute the distance:  Euclidan for now
    // Maybe I wanna do two distances, one per hand?  Or is that the same thing?
    Math.sqrt(distances[0] * distances[0] + distances[1] * distances[1]) => the_distance;
    <<< "The Euclidian distance:  ", the_distance, "\n" >>>;

    // If our conditional deals with gain, I think our life gets much easier..
    // This also means that as we move away from things, we can get louder or softer, if we're doing the 'hunt the timbre' game
    
    // I will need to tune the heck out of this value
    25.0 => float playback_distance;
    if (the_distance > playback_distance) {   
        <<< "Distance above playback_distance, gain is 0.0" >>>;
        0.0 => g.gain;
    }
    if (the_distance == 0) {
        <<< "Distance is zero, gain is 1.0" >>>;
        1.0 => g.gain;
    }
    if (the_distance > 0 && the_distance < playback_distance ) {
        <<< "Distance is between 0 and playback_distance, gain is", 1 - (the_distance / playback_distance) >>>;
        1 - (the_distance / playback_distance) => g.gain;
    }

    // Something cute about scoring here...
    score + the_distance => score;

    // Note that this will break if we take it out of the directory
    path + chunk_filename_base + index + ".wav" => buf.read;  
    buf.length() => now;   
}

