from netdisco.discovery import NetworkDiscovery
import json

def discover():
  netdis = NetworkDiscovery()
  netdis.scan()
  counter = 1
  hosts = {}
  
  for dev in netdis.discover():
    for info in netdis.get_info(dev):
      hosts[counter]  = info
      counter += 1
  netdis.stop()
  final_output = {}
  final_counter = 1
  for k,v in hosts.items():
    temp_str = ""
    for a,b in v.items():
      try: 
        for c,d in b.items():
          each = str(d) + ","
          temp_str += each
      except AttributeError:
        each = str(b) + ","
        temp_str += each
    final_output[final_counter] = temp_str
    final_counter += 1

  
  with open('discover.json','w') as outfile:
    json.dump(final_output, outfile)

  return final_output



