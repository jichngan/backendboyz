import sys
from datetime import datetime 
from scapy.all import *
import requests
import json

'''
try: 
  #interface = raw_input("[*] Enter Desired Interface: ")
  #ips = raw_input("[*] Enter Range of IP address: ")

except KeyboardInterrupt:
  print "\n[*] User Requested Shutdown"
  print "[*] Quitting..."
  sys.exit(1)
'''
def scan():
  interface = "en0"
  ips = "192.168.0.0/24"

  print ("\n[*] Scanning...")
  start_time = datetime.now()

  conf.verb = 0
  ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ips),timeout=1,iface = interface,inter=0.1)

  print ("MAC - IP\n")
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
    '''
    mac_output[counter] = mac
    ip_output[counter] = ip 
    '''
    counter+=1

  stop_time = datetime.now()
  total_time = stop_time - start_time
  for k,v in sorted(final_output.items()):
    print (final_output[k]["IP"])
    print (final_output[k]["Mac"])
    print (final_output[k]["Company"])



  print ("\n[*] Scan Complete!")
  print ("[*] Scan Duration: %s" %(total_time)) 
  with open('scan.json', 'w') as outfile:
    json.dump(final_output, outfile)

  return final_output

