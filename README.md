# Nosy IOT Inspector
## Sometimes it is better to be in the know

## What is Nosy?

Nosy is a Home Network monitoring suite that can scan for all IOT devices connected to the network. Thereafter, users can choose to monitor for the network traffic of a specific IOT device.After monitoring, users can upload a graph of their scan to [Nosy's website] (http://www.nosybackendboyz.com). Currently, Nosy will run on Mac and Linux Operating System.  

## Main Website 

Here are the main features of the main website
- Nosy's Dashboard is hosted locally, this website acts as a platform for users to download the dashboard
- The main website acts as a forum for users to discuss their network findings of their IOT devices
- Users must create an account before posting on the forum or downloading Nosy
- There is also a demo dashboard available for users to try out Nosy before downloading it

## Nosy Dashboard 

Nosy Dashboard is hosted locally using flask servers on port 1234 as well as port 5678. Some of the features that Nosy offers will require basic knowledge of Command Line Interface (CLI) to execute.

Here are the main features of Nosy:
- Scan for all devices connected to network. This scan is placed under the *Discover All* tab. Scan will return IP Address, MAC Address as well as manufacturer of device based on MAC Address
- Scan for IOT devices connected to network. This scan is placed under the *Scan IOT Decice* tab. Scan will return IP Adddress as well as in-depth information of IOT Device. Some of the informaiton will include the name given to the IOT device by the user. Information differs for each IOT Device
- Scan Network Traffic of specific device. This scan requires CLI knowledge and basic information on how to run the scan is displayed in the *Scan Network Traffic* tab. This scan allows users to look at the network traffic of a specific IOT device in real time, traffic the website the IOT Device is visiting against how many bytes of data it is sending out. These information is then plotted on a graph. 
- To view the full graph of previous scan, proceed to *Display Network Traffic* and this will show the previously scanned graph. 

## Instructions to Run Nosy 

1. Sign up on Nosy Website as mentioned above
2. Download the appropriate Nosy for your OS
3. Run ./installation.sh first to install the dependencies needed for Nosy 
4. Run ./run_servers.sh to run Nosy 
5. To perform scan of network traffic, run ./sniff.sh to scan

More instructions can be either found on Nosy's website or on the local dashboard under the *Instructions* tab. 

## Nosy Documentation

To read the full documentation for Nosy, please proceed to (https://docs.google.com/document/d/1z5KLxhMu4rpZFnFV1pzo9JIF8D_qs3g8s6wh41uCCG8/edit?usp=sharing)

Nosy was created as part of National University of Singapore's module titled Orbital: CP2106: Independent Software Development Project.


