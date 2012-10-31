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

// I'll need to fit everything into one message, I think...

while (true) {
    recX => now;
    if (recX.nextMsg() != 0) {
        <<< "from osc: ", recX.getInt()>>>;
    } 
}


