todo:

write output to spreadsheet by location code

~~consider case where the arp table is empty, customer must be alerted to this as well~~

generate clean list of locations with violations

Alan Villarreal - 2020

Scenario: Suppose a customer has a large number of locations with us. They called in and created a ticket with support because they want to ensure that the arp table on the POS (trust) network at all of their locations has only one device (the POS server). If a location has more than 1 device, they want the full arp output of those locations so they can investigate on their end, perhaps by comparing MAC addresses to their list. There are hundreds of locations and doing this manually would be tedious and time consuming. Develop a script to check that the locations have only one device. They want to ensure that an attacker has not inserted a switch into the network and added their own device to the pos environment.

Ideally this customer would have the trust network locked down such that the specified host is the only thing allowed, however they have not provided this information and had us configure a /24 despite only needing 1 address.

I am assuming that we already have an inventory file maintained for this customer, otherwise we might take a spreadsheet mapping location codes to loopbacks (how we access these devices over our VPN) and dynamically create an inventory file.

In this case, the trust network is on Ethernet 0/3. We can ignore the gateway.

INPUT:

A list of dictionaries built from the output of the nornir AggregatedResult object.

~~~
This is sanitized output of the AggregatedResult object returned by nornir
>>> for x in result:
...     print(x)
...     for k in result[x].result['get_arp_table']:
...             print(k)

ABC-001-0001
{'interface': 'Ethernet0/0', 'mac': '0C:13:B8:43:CC:01', 'ip': '192.168.10.1', 'age': 34.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:00', 'ip': '192.168.10.2', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:01:10', 'ip': '192.168.10.5', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:02:00', 'ip': '192.168.10.6', 'age': 51.0}
{'interface': 'Ethernet0/2', 'mac': 'AA:BB:CC:00:01:20', 'ip': '192.168.10.17', 'age': 0.0}
{'interface': 'Ethernet0/2', 'mac': 'AA:BB:CC:00:03:00', 'ip': '192.168.10.18', 'age': 36.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:01:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:00', 'ip': '192.168.30.2', 'age': 171.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:04', 'ip': '192.168.30.20', 'age': 7.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:05', 'ip': '192.168.30.21', 'age': 218.0}
ABC-001-0002
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:10', 'ip': '192.168.10.5', 'age': 51.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:02:00', 'ip': '192.168.10.6', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:02:10', 'ip': '192.168.10.9', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:00', 'ip': '192.168.10.10', 'age': 36.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:02:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:01', 'ip': '192.168.30.3', 'age': 172.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:06', 'ip': '192.168.30.50', 'age': 166.0}
ABC-001-0003
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:10', 'ip': '192.168.10.13', 'age': 36.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:03:10', 'ip': '192.168.10.14', 'age': 0.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:20', 'ip': '192.168.10.17', 'age': 36.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:03:00', 'ip': '192.168.10.18', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:03:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:02', 'ip': '192.168.30.4', 'age': 171.0}
ABC-001-0004
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:02:10', 'ip': '192.168.10.9', 'age': 36.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:04:00', 'ip': '192.168.10.10', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:10', 'ip': '192.168.10.13', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:03:10', 'ip': '192.168.10.14', 'age': 36.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:04:30', 'ip': '192.168.30.1', 'age': 0.0}
~~~
Output:

List containing dictionaries which make up the arp table of locations with mac address violations
List containing location codes with empty arp tables

~~~
We have found violations of the # of mac addresses policy on Ethernet 0/3 across 2 locations. The full arp output of Ethernet 0/3 for all offending locations will be printed below
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:04', 'ip': '192.168.30.20', 'age': 10.0}}
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:00', 'ip': '192.168.30.2', 'age': 174.0}}
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:05', 'ip': '192.168.30.21', 'age': 221.0}}
{'ABC-001-0002': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:06', 'ip': '192.168.30.50', 'age': 168.0}}
{'ABC-001-0002': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:01', 'ip': '192.168.30.3', 'age': 175.0}}

The following locations have an empty arp table on Ethernet 0/3, indicating that there may be nothing plugged into the trust network, or whatever is on the trust network is not replying to ARP
ABC-001-0004
~~~