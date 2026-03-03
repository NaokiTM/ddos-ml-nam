#!/bin/bash

# this is only used for my own personal computer, though it may work on other computers I just havent looked into it enough. 
# the directory names are different because I move the files to be tested into the POX directory later which is named differently


# mininet cleanup for old instances 
sudo mn -c > /dev/null 2>&1

# remove the process used on port 6633 (which is the default POX controller port)
sudo fuser -k 6633/tcp > /dev/null 2>&1

# Start POX and load windowCheck (the first) module (for now, we later stack the modules im guessing?)
python3 ./pox.py log.level --DEBUG fmdadm.windowCheck > pox.log 2>&1 &
python3 ./pox.py log.level --DEBUG fmdadm.windowCheck > pox.log 2>&1 &
sleep 3

# Start Mininet with 5 hosts, 1 switch, controller on localhost
sudo mn --topo single,5 --controller=remote,ip=127.0.0.1,port=6633 --mac > mn.log 2>&1 &
MN_PID=$!
sleep 5  # Give Mininet time to initialize

# Example: Launch SYN flood from h1 to h5 (target host)
sudo mnexec -a $(pgrep -f "mininet:h1") hping3 -S --flood -p 80 10.0.0.5 > flood_h1.log 2>&1 &

# Let attack run for 15 seconds
sleep 15

# Stop attacks
kill $HPING1_PID
kill $HPING2_PID

# Store Process id so we can kill it when script finishes
POX_PID=$!
sudo mn -c > /dev/null 2>&1