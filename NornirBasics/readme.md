todo:

Instead of just pasting the output of the program, I will show the code and output together

~~~
~/AutomationScenarios/NornirBasics$ python3 nornirbasics.py 
First lets look at the type of the result object with type(task_result):  nornir.core.task.AggregatedResult 

Then the output of print(task_result):  AggregatedResult (napalm_get): {'Router1': MultiResult: [Result: "napalm_get"], 'Router2': MultiResult: [Result: "napalm_get"], 'Router3': MultiResult: [Result: "napalm_get"], 'Router4': MultiResult: [Result: "napalm_get"]}
******************************************************************************************************************************************************
We can access the MultiResult objects within the AggregatedResult by using the hostnames as the key, here I will do type(task_result['Router1']):  nornir.core.task.MultiResult

Lets look at the output of print(task_result['Router1']):  MultiResult: [Result: "napalm_get"]
******************************************************************************************************************************************************
We can unpack the Multiresult object with the .result method, lets do type(task_result['Router1'].result):   <class 'dict'> 

Now the output of print(result.task_result):  {'facts': {'uptime': 43920, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Serial2/0', 'Serial2/1', 'Serial2/2', 'Serial2/3', 'Serial3/0', 'Serial3/1', 'Serial3/2', 'Serial3/3', 'Loopback0']}}
******************************************************************************************************************************************************
Now we have visibility into the dictionaries that make up the output of the nornir task that we ran, we can construct a simple loop to display all of the Hostnames and their associated dictionaries in a neat fashion: 

<class 'str'>
Router1
<class 'dict'>
{'facts': {'uptime': 43920, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Serial2/0', 'Serial2/1', 'Serial2/2', 'Serial2/3', 'Serial3/0', 'Serial3/1', 'Serial3/2', 'Serial3/3', 'Loopback0']}}
<class 'str'>
Router2
<class 'dict'>
{'facts': {'uptime': 43920, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048002', 'model': 'Unknown', 'hostname': 'ABC-001-0002', 'fqdn': 'ABC-001-0002.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Serial2/0', 'Serial2/1', 'Serial2/2', 'Serial2/3', 'Serial3/0', 'Serial3/1', 'Serial3/2', 'Serial3/3', 'Loopback0']}}
<class 'str'>
Router3
<class 'dict'>
{'facts': {'uptime': 43920, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048003', 'model': 'Unknown', 'hostname': 'ABC-001-0003', 'fqdn': 'ABC-001-0003.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Serial2/0', 'Serial2/1', 'Serial2/2', 'Serial2/3', 'Serial3/0', 'Serial3/1', 'Serial3/2', 'Serial3/3', 'Loopback0']}}
<class 'str'>
Router4
<class 'dict'>
{'facts': {'uptime': 13500, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048004', 'model': 'Unknown', 'hostname': 'ABC-001-0004', 'fqdn': 'ABC-001-0004.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Serial2/0', 'Serial2/1', 'Serial2/2', 'Serial2/3', 'Serial3/0', 'Serial3/1', 'Serial3/2', 'Serial3/3', 'Loopback0', 'Loopback1']}}
We can clean this up a bit with json.dumps
Router1
{
    "facts": {
        "uptime": 43920,
        "vendor": "Cisco",
        "os_version": "Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE",
        "serial_number": "2048001",
        "model": "Unknown",
        "hostname": "ABC-001-0001",
        "fqdn": "ABC-001-0001.lab.com",
        "interface_list": [
            "Ethernet0/0",
            "Ethernet0/1",
            "Ethernet0/2",
            "Ethernet0/3",
            "Ethernet1/0",
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/3",
            "Serial2/0",
            "Serial2/1",
            "Serial2/2",
            "Serial2/3",
            "Serial3/0",
            "Serial3/1",
            "Serial3/2",
            "Serial3/3",
            "Loopback0"
        ]
    }
}
Router2
{
    "facts": {
        "uptime": 43920,
        "vendor": "Cisco",
        "os_version": "Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE",
        "serial_number": "2048002",
        "model": "Unknown",
        "hostname": "ABC-001-0002",
        "fqdn": "ABC-001-0002.lab.com",
        "interface_list": [
            "Ethernet0/0",
            "Ethernet0/1",
            "Ethernet0/2",
            "Ethernet0/3",
            "Ethernet1/0",
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/3",
            "Serial2/0",
            "Serial2/1",
            "Serial2/2",
            "Serial2/3",
            "Serial3/0",
            "Serial3/1",
            "Serial3/2",
            "Serial3/3",
            "Loopback0"
        ]
    }
}
Router3
{
    "facts": {
        "uptime": 43920,
        "vendor": "Cisco",
        "os_version": "Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE",
        "serial_number": "2048003",
        "model": "Unknown",
        "hostname": "ABC-001-0003",
        "fqdn": "ABC-001-0003.lab.com",
        "interface_list": [
            "Ethernet0/0",
            "Ethernet0/1",
            "Ethernet0/2",
            "Ethernet0/3",
            "Ethernet1/0",
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/3",
            "Serial2/0",
            "Serial2/1",
            "Serial2/2",
            "Serial2/3",
            "Serial3/0",
            "Serial3/1",
            "Serial3/2",
            "Serial3/3",
            "Loopback0"
        ]
    }
}
Router4
{
    "facts": {
        "uptime": 13500,
        "vendor": "Cisco",
        "os_version": "Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE",
        "serial_number": "2048004",
        "model": "Unknown",
        "hostname": "ABC-001-0004",
        "fqdn": "ABC-001-0004.lab.com",
        "interface_list": [
            "Ethernet0/0",
            "Ethernet0/1",
            "Ethernet0/2",
            "Ethernet0/3",
            "Ethernet1/0",
            "Ethernet1/1",
            "Ethernet1/2",
            "Ethernet1/3",
            "Serial2/0",
            "Serial2/1",
            "Serial2/2",
            "Serial2/3",
            "Serial3/0",
            "Serial3/1",
            "Serial3/2",
            "Serial3/3",
            "Loopback0",
            "Loopback1"
        ]
    }
}

However nornir comes with a print_result function that we can use on our original task_result, which saves us the trouble of accessing the data ourselves, unless we need the underlying data for some other logic. Here is the output of print_result(task_result): 

napalm_get**********************************************************************
* Router1 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'ABC-001-0001.lab.com',
             'hostname': 'ABC-001-0001',
             'interface_list': [ 'Ethernet0/0',
                                 'Ethernet0/1',
                                 'Ethernet0/2',
                                 'Ethernet0/3',
                                 'Ethernet1/0',
                                 'Ethernet1/1',
                                 'Ethernet1/2',
                                 'Ethernet1/3',
                                 'Serial2/0',
                                 'Serial2/1',
                                 'Serial2/2',
                                 'Serial2/3',
                                 'Serial3/0',
                                 'Serial3/1',
                                 'Serial3/2',
                                 'Serial3/3',
                                 'Loopback0'],
             'model': 'Unknown',
             'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), '
                           'Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE',
             'serial_number': '2048001',
             'uptime': 43920,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router2 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'ABC-001-0002.lab.com',
             'hostname': 'ABC-001-0002',
             'interface_list': [ 'Ethernet0/0',
                                 'Ethernet0/1',
                                 'Ethernet0/2',
                                 'Ethernet0/3',
                                 'Ethernet1/0',
                                 'Ethernet1/1',
                                 'Ethernet1/2',
                                 'Ethernet1/3',
                                 'Serial2/0',
                                 'Serial2/1',
                                 'Serial2/2',
                                 'Serial2/3',
                                 'Serial3/0',
                                 'Serial3/1',
                                 'Serial3/2',
                                 'Serial3/3',
                                 'Loopback0'],
             'model': 'Unknown',
             'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), '
                           'Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE',
             'serial_number': '2048002',
             'uptime': 43920,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router3 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'ABC-001-0003.lab.com',
             'hostname': 'ABC-001-0003',
             'interface_list': [ 'Ethernet0/0',
                                 'Ethernet0/1',
                                 'Ethernet0/2',
                                 'Ethernet0/3',
                                 'Ethernet1/0',
                                 'Ethernet1/1',
                                 'Ethernet1/2',
                                 'Ethernet1/3',
                                 'Serial2/0',
                                 'Serial2/1',
                                 'Serial2/2',
                                 'Serial2/3',
                                 'Serial3/0',
                                 'Serial3/1',
                                 'Serial3/2',
                                 'Serial3/3',
                                 'Loopback0'],
             'model': 'Unknown',
             'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), '
                           'Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE',
             'serial_number': '2048003',
             'uptime': 43920,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router4 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'ABC-001-0004.lab.com',
             'hostname': 'ABC-001-0004',
             'interface_list': [ 'Ethernet0/0',
                                 'Ethernet0/1',
                                 'Ethernet0/2',
                                 'Ethernet0/3',
                                 'Ethernet1/0',
                                 'Ethernet1/1',
                                 'Ethernet1/2',
                                 'Ethernet1/3',
                                 'Serial2/0',
                                 'Serial2/1',
                                 'Serial2/2',
                                 'Serial2/3',
                                 'Serial3/0',
                                 'Serial3/1',
                                 'Serial3/2',
                                 'Serial3/3',
                                 'Loopback0',
                                 'Loopback1'],
             'model': 'Unknown',
             'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), '
                           'Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE',
             'serial_number': '2048004',
             'uptime': 13500,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~~~