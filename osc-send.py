#!/usr/bin/python

import OSC

client = OSC.OSCClient()
client.connect( ('127.0.0.1', 7777) ) # note that the argument is a tupple and not two arguments
msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
msg.setAddress("/timbre/1/")
msg.append(1.1)
client.send(msg) # now we dont need to tell the client the address anymore

