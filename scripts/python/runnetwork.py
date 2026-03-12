import subprocess
import time
import sys
import getpass

# unsecure so change later
password = getpass.getpass("Enter sudo password: ")
module = input("Enter module: ")

TERM_1_COMMANDS = (f"""
    sudo -S fuser -k 6633/tcp; 
    cd /home/lilliput/pox && 
    python3 ./pox.py log.level --DEBUG --WARNING=forwarding.l2_learning openflow.of_01 forwarding.l2_learning fmdadm.{module}
""").strip()

TERM_2_COMMANDS = "sudo -S mn --topo single,5 --controller=remote,ip=127.0.0.1,port=6633 --mac"

MN_COMMANDS = "\n".join([
    "h1 hping3 -S --flood -p 80 10.0.0.2", 
    "sh sleep 15", 
    "h1 kill %hping3",
])

term1 = subprocess.Popen(TERM_1_COMMANDS, shell=True, stdin=subprocess.PIPE)
term1.stdin.write((password + "\n").encode())
term1.stdin.flush()

# give POX time to bind 6633 before starting mininet
time.sleep(5)

term2 = subprocess.Popen(TERM_2_COMMANDS, shell=True, stdin=subprocess.PIPE)
term2.stdin.write((password + "\n").encode())
term2.stdin.flush()

# give mininet time to start before piping commands in
time.sleep(10)

term2.stdin.write((MN_COMMANDS + "\n").encode())
term2.stdin.flush()

term2.wait()
term1.terminate()