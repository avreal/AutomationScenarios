todo:

write output to spreadsheet by location code

Alan Villarreal - 2020

Scenario: Suppose a customer has a large number of locations with us. They called in and created a ticket with support because they want to ensure that the arp table on the POS (trust) network at all of their locations has only one device (POS server). If a location has more than 1 device, they want the full arp output of those locations so they can investigate on their end (comparing MACs). There are hundreds of locations and doing this manually would be tedious and time consuming. Develop a script to check that the locations have only one device. They want to ensure that an attacker has not inserted a switch into the network and added their own device to the pos environment.

Ideally this customer would have the trust network locked down such that the specified host is the only thing allowed, however they have not provided this information and had us configure a /24 despite only needing 1 address.

I am assuming that we already have an inventory file maintained for this customer, otherwise me might take a spreadsheet mapping location codes to loopbacks (how we access these devices over our VPN) and dynamically create an inventory.

In this case, the trust network is on Ethernet 0/3. We can ignore the gateway.

INPUT:

This is sanitized output of the AggregatedResult object returned by nornir

ABC-001-0001
{'interface': 'Ethernet0/0', 'mac': '0C:13:B8:43:CC:01', 'ip': '192.168.10.1', 'age': 218.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:00', 'ip': '192.168.10.2', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:01:10', 'ip': '192.168.10.5', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:02:00', 'ip': '192.168.10.6', 'age': 211.0}
{'interface': 'Ethernet0/2', 'mac': 'AA:BB:CC:00:01:20', 'ip': '192.168.10.17', 'age': 0.0}
{'interface': 'Ethernet0/2', 'mac': 'AA:BB:CC:00:03:00', 'ip': '192.168.10.18', 'age': 217.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:01:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:00', 'ip': '192.168.30.2', 'age': 89.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:04', 'ip': '192.168.30.20', 'age': 191.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:05', 'ip': '192.168.30.21', 'age': 136.0}
ABC-001-0002
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:10', 'ip': '192.168.10.5', 'age': 211.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:02:00', 'ip': '192.168.10.6', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:02:10', 'ip': '192.168.10.9', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:00', 'ip': '192.168.10.10', 'age': 217.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:02:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:01', 'ip': '192.168.30.3', 'age': 90.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:06', 'ip': '192.168.30.50', 'age': 84.0}
ABC-001-0003
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:10', 'ip': '192.168.10.13', 'age': 217.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:03:10', 'ip': '192.168.10.14', 'age': 0.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:01:20', 'ip': '192.168.10.17', 'age': 217.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:03:00', 'ip': '192.168.10.18', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:03:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:02', 'ip': '192.168.30.4', 'age': 88.0}
ABC-001-0004
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:02:10', 'ip': '192.168.10.9', 'age': 217.0}
{'interface': 'Ethernet0/0', 'mac': 'AA:BB:CC:00:04:00', 'ip': '192.168.10.10', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:04:10', 'ip': '192.168.10.13', 'age': 0.0}
{'interface': 'Ethernet0/1', 'mac': 'AA:BB:CC:00:03:10', 'ip': '192.168.10.14', 'age': 217.0}
{'interface': 'Ethernet0/3', 'mac': 'AA:BB:CC:00:04:30', 'ip': '192.168.30.1', 'age': 0.0}
{'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:03', 'ip': '192.168.30.5', 'age': 105

Output:

We have found 5 violations of the # of mac addresses policy across 2 locations. The full arp output for all offending locations will be printed below
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:04', 'ip': '192.168.30.20', 'age': 191.0}}
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:00', 'ip': '192.168.30.2', 'age': 89.0}}
{'ABC-001-0001': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:05', 'ip': '192.168.30.21', 'age': 136.0}}
{'ABC-001-0002': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:06', 'ip': '192.168.30.50', 'age': 84.0}}
{'ABC-001-0002': {'interface': 'Ethernet0/3', 'mac': '00:50:79:66:68:01', 'ip': '192.168.30.3', 'age': 90.0}}
