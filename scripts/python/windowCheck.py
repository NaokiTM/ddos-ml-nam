import math
from pox.core import core
import pox.openflow.libopenflow_01 as of

# we chose 32 packet window size because it's proven to be best for detecting meaningful entropy changes
WINDOWSIZE = 32

# example threshold, change later
THRESHOLD = 1
windowBuffer = {}
 
# using shannons entropy formula
def calculateEntropy(buffer):
    counts = {ip: buffer.count(ip) for ip in set(buffer)}

    entropy = 0
    for count in counts.values():
        p = count / len(buffer)
        entropy -= p * math.log2(p)
    return entropy

# calculating the window entropy based on packet source IP table
def calculateAwedr(buffer):
    awae = calculateEntropy(buffer)
    awne = calculateEntropy(buffer)
    awedr = ((awne-awae) / awne) * 100 if awne != 0 else 0
    return awedr


# a small function to handle a single new packet when it passes through (this counts as one event)
def handlePackets(event):
    newPacket = event.parsed
    switchId = event.dpid

    ip_packet = newPacket.find('ipv4')
    if ip_packet is None:
        return

    packetSourceIp = ip_packet.src

    if switchId not in windowBuffer:
        windowBuffer[switchId] = []

    windowBuffer[switchId].append(str(ip_packet.dst))

    if (len(windowBuffer[switchId]) == WINDOWSIZE):

        entropy = calculateAwedr(windowBuffer[switchId])

        if (entropy > THRESHOLD):
            flowModObj = of.ofp_flow_mod()
            flowModObj.priority = 65535
            flowModObj.match.nw_src = packetSourceIp
            event.connection.send(flowModObj)

        windowBuffer[switchId] = []


def launch():
    core.openflow.addListenerByName("PacketIn", handlePackets)

