import sys
from datetime import datetime 
#from scapy.all import srp, Ether, ARP, conf
from scapy.all import *

'''
try: 
  #interface = raw_input("[*] Enter Desired Interface: ")
  #ips = raw_input("[*] Enter Range of IP address: ")

except KeyboardInterrupt:
  print "\n[*] User Requested Shutdown"
  print "[*] Quitting..."
  sys.exit(1)
'''

interface = "wlan0"
ips = "192.168.0.0/24"

print "\n[*] Scanning..."
start_time = datetime.now()

conf.verb = 0
ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ips),timeout=2,iface = interface,inter=0.1)

print "MAC - IP\n"
counter = 1
for snd,rcv in ans:
    mac_address = "Mac Address of device " + str(counter) + " :"
    sys.stdout.write(mac_address)
    print rcv.sprintf("%Ether.src%")
    ip_address = "IP Address of device " + str(counter) + " :"
    sys.stdout.write(ip_address)
    print rcv.sprintf("%ARP.psrc%")
    counter+=1

stop_time = datetime.now()
total_time = stop_time - start_time 

print "\n[*] Scan Complete!"
print ("[*] Scan Duration: %s" %(total_time)) 

