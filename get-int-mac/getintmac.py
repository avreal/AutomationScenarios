"""
Alan Villarreal - 2020

Scenario: Suppose a customer has a large number of locations with us. They called in and created a ticket with support because
they want to ensure that the arp table on the POS (trust) network at all of their locations has only one device (POS server). 
They also want to make sure that mac addres matches what is in their own database. There are hundreds of locations and doing this 
manually would be tedious and time consuming. Develop a script that will read a spreadsheet with the location code, loopback, mac address
and will write a file which indicates which locations do not meet the criteria.

"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import json

nr = InitNornir(config_file="./config.yaml")
result = nr.run(task=napalm_get,getters=["get_arp_table"])

print_result(result)