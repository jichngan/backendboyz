from netdisco.discovery import NetworkDiscovery

def discover():
  netdis = NetworkDiscovery()

  print("Start Scan...")
  netdis.scan()
  counter = 1
  hosts = {}
  for dev in netdis.discover():
#    print (type(dev))
#    print (dev)
#    print(type(netdis.get_info(dev)))
#    print (netdis.get_info(dev))
    for info in netdis.get_info(dev):
#      print (type(info))
#      print (info)
      hosts[counter]  = info
      counter += 1
#  print ("+++++++++++++++++++++++++++++++++++++++++++++++++++")
#  for k,v in hosts.items():
#    print (k,"->",v)
  print("Scanning complete...")
  netdis.stop()
  final_output = {}
  final_counter = 1
  for k,v in hosts.items():
    temp_str = ""
    for a,b in v.items():
      try: 
        for c,d in b.items():
          each = str(d) + "/"
          temp_str += each
      except AttributeError:
        each = str(b) + "/"
        temp_str += each
    final_output[final_counter] = temp_str
    final_counter += 1

  return final_output



