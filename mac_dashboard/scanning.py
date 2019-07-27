'''
Code to scan for all devices connected to the network 
User will have to change interface and IPs to suit their network but the one used here is the generic case
This also saves the output into a Json file 
There is also an API to check for manufacturer of product 
'''

import sys
from scapy.all import *
import requests
import json

def scan():
  #**EDIT HERE** If your interface is NOT Wlan0 
  interface = "en0"
  ips = "192.168.0.0/24"

  conf.verb = 0
  ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ips),timeout=1,iface = interface,inter=0.1)

  counter = 1
  mac_output = {} #Dictionary for mac output
  ip_output = {} #Dictionary for IP output
  final_output = {}
  for snd,rcv in ans:
    mac = rcv.sprintf("%Ether.src%")
    ip = rcv.sprintf("%ARP.psrc%")
    vendor = requests.get('http://macvendors.co/api/' + mac).text
    d = json.loads(vendor)
    final_output[counter] = {}
    final_output[counter]["Mac"] = mac
    final_output[counter]["IP"] = ip
    final_output[counter]["Company"] = d['result']['company']
    counter+=1

  with open('scan.json', 'w') as outfile:
    json.dump(final_output, outfile)

  return final_output

