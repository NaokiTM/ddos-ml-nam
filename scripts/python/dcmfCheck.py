import math
from pox.core import core
import pox.openflow.libopenflow_01 as openflow

# declared globally for persistence across all passing packets
macSet = {}   # called S_te1 in the paper's psuedocode
ipSet = {}   # called S_te2 in the paper's psuedocode

# ran for each passing packet 
def dcmfCheck(event):

    packet = event.parsed
    ipPacket = packet.find('ipv4')

    # a check to ensure the packet is ipv4 before proceeding
    if ipPacket:
        sourceIp = ipPacket.srcip
        sourceMac = packet.src         
    else:
        return
    if sourceIp not in macSet:
        # create a new set of associated mac addresses for the source IP if it doesnt already exist
        macSet[sourceIp] = set()

    # create the initial 1 to 1 source IP -> source MAC pairing
    macSet[sourceIp].add(sourceMac)
    if sourceMac not in ipSet:
        # create a new set of associated IP addresses for the source MAC if it doesnt already exist
        ipSet[sourceMac] = set()

    # create the initial 1 to 1 source MAC-> source IP pairing
    ipSet[sourceMac].add(sourceIp)


    # deemed attack if one source ip/mac has > 1 associated mac/ip
    if len(macSet[sourceIp]) > 1:  # forged IP
        flowMod = openflow.ofp_flow_mod()
        flowMod.priority = 65535
        flowMod.match.nw_src = str(sourceIp)
        flowMod.actions = []  # drop
        event.connection.send(flowMod)
        print(f"Blocked IP {sourceIp} (multiple MACs: {macSet[sourceIp]})")

    elif len(ipSet[sourceMac]) > 1: # forged MAC
        flowMod = openflow.ofp_flow_mod()
        flowMod.priority = 65535
        flowMod.match.dl_src = str(sourceMac)
        flowMod.actions = []  # drop
        event.connection.send(flowMod)
        print(f"Blocked MAC {sourceMac} (multiple IPs: {ipSet[sourceMac]})")

# copied from the first module, check if its correct later
def launch():
    core.openflow.addListenerByName("PacketIn", dcmfCheck)