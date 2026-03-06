import math
from pox.core import core
import pox.openflow.libopenflow_01 as openflow

# we chose 32 packet window size because it's proven to be best for detecting meaningful entropy changes
WINDOWSIZE = 32

# example threshold, change later
THRESHOLD = 1

currentWindow = {}

# using shannons entropy formula
def calculateEntropy(window):
    counts = {ip: window.count(ip) for ip in set(window)}
    entropy = 0
    for count in counts.values():
        p = count / len(window)
        entropy -= p * math.log2(p)
    return entropy

# calculating the window entropy based on packet source IP table
def calculateAwedr(window):
    awae = calculateEntropy(window)
    awne = calculateEntropy(window)
    awedr = ((awne-awae) / awne) * 100 if awne != 0 else 0
    return awedr

# a small function to handle a single new packet when it passes through (this counts as one event)
def handlePackets(event):
    newPacket = event.parsed
    switchId = event.dpid
    ip_packet = newPacket.find('ipv4')

    if ip_packet is None:
        return
    
    packetSourceIp = ip_packet.srcip

    if switchId not in currentWindow:
        currentWindow[switchId] = []

    currentWindow[switchId].append(str(ip_packet.srcip))

    if (len(currentWindow[switchId]) == WINDOWSIZE):
        entropy = calculateEntropy(currentWindow[switchId])
        if (entropy < THRESHOLD):
            flowModObj = openflow.ofp_flow_mod()
            flowModObj.priority = 65535
            flowModObj.match.nw_src = str(packetSourceIp)
            flowModObj.actions = []  # drop
            event.connection.send(flowModObj)
            print(f"Blocked suspicious source {packetSourceIp} (entropy={entropy:.3f})")
        else:
            print("safe window")
        currentWindow[switchId] = []

def launch():
    core.openflow.addListenerByName("PacketIn", handlePackets)