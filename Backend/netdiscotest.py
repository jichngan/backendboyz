from netdisco.discovery import NetworkDiscovery


netdis = NetworkDiscovery()

print("Start Scan...")
print('\n')
netdis.scan()
counter = 1
for dev in netdis.discover():
    for info in netdis.get_info(dev):
      print("Device Number: " + str(counter))
      print(dev)
      print("Host: " + str(info['host']))
      print("Hostname: " + str(info['hostname']))
      print("Name of Device: " + str(info['properties']['md']))
      print("User given name: " + str(info['properties']['fn']))
      if (str(info['properties']['rs']) != "False"):
        print("Currently on: " + str (info['properties']['rs']))
      print('\n')
      counter+=1


print("Scanning complete...")
netdis.stop()

