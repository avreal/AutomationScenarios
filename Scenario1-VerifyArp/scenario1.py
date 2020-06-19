"""
Alan Villarreal - 2020

See readme for scenario explanation

"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="./config.yaml")
result = nr.run(task=napalm_get,getters=["get_arp_table"])

#The full napalm output can be printed if needed as well
#print_result(result)

#create a list of entries specifying not to include the gateway IP and only checking interface Ethernet0/3
#locations with nothing in the arp table besides the interface itself on Ethernet 0/3 will be added to a separate list
arp_list = []
empty_arp_list = []
for x in result:
    for k in result[x].result['get_arp_table']:
        tmp_list = []
        if (k['interface'] == "Ethernet0/3") and (k['ip'] != "192.168.30.1"):
            arp_list.append({x:k})
            tmp_list.append({x:k})
    if len(tmp_list) == 0:
        empty_arp_list.append(x)

# This function will go through the result and create a list with the violations pertaining to having more than 1 MAC on the interface
total_entries = len(arp_list)
num_violation_locations = 0
violation_list = []
new_location_flag = True
for i in range(total_entries):
    if i == 0:
        continue
    elif arp_list[i].keys() == arp_list[i-1].keys() and new_location_flag == True:
        violation_list.append(arp_list[i])
        violation_list.append(arp_list[i-1])
        num_violation_locations += 1
        new_location_flag = False
    elif arp_list[i].keys() == arp_list[i-1].keys() and new_location_flag == False:
        violation_list.append(arp_list[i])
    elif arp_list[i].keys() != arp_list[i-1].keys():
        new_location_flag = True

print("We have found violations of the # of mac addresses policy on Ethernet 0/3 across", num_violation_locations, "locations. The full arp output of Ethernet 0/3 for all offending locations will be printed below")
for i in violation_list:
    print(i)

print("\nThe following locations have an empty arp table on Ethernet 0/3, indicating that there may be nothing plugged into the trust network, or whatever is on the trust network is not replying to ARP\n")
for i in empty_arp_list:
    print(i)




