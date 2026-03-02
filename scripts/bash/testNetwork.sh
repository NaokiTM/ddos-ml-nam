#!/bin/bash

# this is only used for my own personal computer, though it may work on other computers I just havent looked into it enough. 


# mininet cleanup for old instances 
sudo mn -c > /dev/null 2>&1

# remove the process used on port 6633 (which is the default POX controller port)
sudo fuser -k 6633/tcp > /dev/null 2>&1

# Start POX and load windowCheck (the first) module (for now, we later stack the modules im guessing?)
python3 ./pox.py log.level --DEBUG fmdadm.windowCheck > pox.log 2>&1 &

# Store Process id so we can kill it when script finishes
POX_PID=$!
