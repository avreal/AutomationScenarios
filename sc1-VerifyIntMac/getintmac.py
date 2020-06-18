"""
Alan Villarreal - 2020

Scenario: Suppose a customer has a large number of locations with us. They called in and created a ticket with support because
they want to ensure that the arp table on the POS (trust) network at all of their locations has only one device (POS server). If a location
has more than 1 device, they want the full arp output of those locations so they can investigate on their end (comparing MACs). 
There are hundreds of locations and doing this manually would be tedious and time consuming. Develop a script to check that the locations 
have only one device. They want to ensure that an attacker has not inserted a switch into the network and added their own device to 
the pos environment.

Ideally this customer would have the trust network locked down such that the specified host is the only thing allowed,
however they have not provided this information and had us configure a /24 despite only needing 1 address.

I am assuming that we already have an inventory file maintained for this customer, otherwise me might take a spreadsheet mapping 
location codes to loopbacks (how we access these devices over our VPN) and dynamically create an inventory.

In this case, the trust network is on Ethernet 0/3. We can ignore the gateway.

"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import json

nr = InitNornir(config_file="./config.yaml")
result = nr.run(task=napalm_get,getters=["get_arp_table"])

#The full napalm output can be printed if needed as well
#print_result(result)

#create a list of entries specifying not to include the gateway IP and only checking interface Ethernet0/3
newlist = []
for x in result:
    for k in result[x].result['get_arp_table']:
        if (k['interface'] == "Ethernet0/3") and (k['ip'] != "192.168.30.1"):
            newlist.append({x:k})

# This function will go through the result and create a list with the violations pertaining to having more than 1 MAC on the interface
totalEntries = len(newlist)
numViolationCount = 0
numViolationLocations = 0
violationList = []
newLocation = True
listlist = []
for i in range(totalEntries):
    if i == 0:
        continue
    elif newlist[i].keys() == newlist[i-1].keys() and newLocation == True:
        violationList.append(newlist[i])
        violationList.append(newlist[i-1])
        numViolationCount += 2
        numViolationLocations += 1
        newLocation = False
    elif newlist[i].keys() == newlist[i-1].keys() and newLocation == False:
        violationList.append(newlist[i])
        numViolationCount += 1
    elif newlist[i].keys() != newlist[i-1].keys():
        newLocation = True

print("We have found violations of the # of mac addresses policy on Ethernet 0/3 across", numViolationLocations, "locations. The full arp output for all offending locations will be printed below")

for i in violationList:
    print(i)




