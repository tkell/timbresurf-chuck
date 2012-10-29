"test.txt" => string inFilename;

FileIO @ in;
new FileIO @=> in;
in.open( inFilename, FileIO.READ );

in.readLine() => string theLine; // read a line
<<< theLine >>>;
in.close();
