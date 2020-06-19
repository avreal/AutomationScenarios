# An Interactive Look At Nornir

## The following is an interactive look at the objects and basic functions we use when creating a nornir task, as well as the output objects that we can deconstruct to access data for parsing.

First we instantiate the InitNornir class, here we can specify a config file or pass the contents as parameters. We then use the run function to execute the task over the hosts in the inventory. In this case I am using the get_facts function from NAPALM.

~~~python
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import json

nr = InitNornir(config_file="./config.yaml")
task_result = nr.run(task=napalm_get,getters=["facts"])
~~~

Lets look at the output of type() for these 2 items.

~~~python
>>> type(nr)
<class 'nornir.core.Nornir'>
>>>
>>> type(task_result)
nornir.core.task.AggregatedResult
>>>
~~~

Suppose we wish to grab certain keys/values from this output for a particular device, we can dig further into the AggregatedResult object that was returned from nr.run. First lets do a normal print(task_result)

~~~python
>>> print(task_result)
AggregatedResult (napalm_get): {'Router1': MultiResult: [Result: "napalm_get"], 'Router2': MultiResult: [Result: "napalm_get"], 'Router3': MultiResult: [Result: "napalm_get"], 'Router4': MultiResult: [Result: "napalm_get"]}
~~~

Here we see that the AggregatedResult object is a dict-like object, we can access the individual MultiResult objects by doing task_result['*hostname*'].

~~~python
>>> task_result['Router1']
MultiResult: [Result: "napalm_get"]
~~~

Now we have a list-like object, in order to extract data from this we can call the .result method as follows

~~~python
>>> task_result['Router1'].result
{'facts': {'uptime': 9600, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Loopback0']}}
>>> 
~~~

Now we have a standard dictionary that we can access data from by using its key(s). See below:

~~~python
>>> output = task_result['Router1'].result
>>>
>>> output['facts']
{'uptime': 9600, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3','Loopback0']}
>>>
>>> output['facts']['uptime']
9600
~~~

Given all of the above, we can now iterate through the Aggregated result object with a nested loop to generate an output with the device hostname and all of the data gathered in the MultiResult object. There are several ways to achieve a similar result.

In this first loop, we print out the hostname as a string then follow it with a nested dictionary where we can then access keys as needed.

~~~python
>>> for host in task_result:
...     print(host)
...     for results in task_result[host]:
...             print(results)
... 
Router1
{'facts': {'uptime': 9600, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Loopback0']}}
Router2

...omitted...

Router3

...omitted...

Router4

...omitted...

~~~

In this example, we use the items() function (recall that AggregatedResult is a dict-like object) and then iterate through the dict_items object we obtain. Since this contains tuples we use an index to access the objects.

~~~python
>>> resultsitems = task_result.items()
>>> for hosts in resultsitems:
...     print(hosts[0])
...     print(hosts[1].result)
... 
Router1
{'facts': {'uptime': 9600, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE', 'serial_number': '2048001', 'model': 'Unknown', 'hostname': 'ABC-001-0001', 'fqdn': 'ABC-001-0001.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3', 'Ethernet1/0', 'Ethernet1/1', 'Ethernet1/2', 'Ethernet1/3', 'Loopback0']}}
Router2

...omitted...

Router3

...omitted...

Router4

...omitted...

>>> 
~~~

In this example, we use a similar loop to example 1 but format the output with json.

~~~python
import json

for hosts in task_result:
    print(hosts)
    for results in task_result[hosts]:
        print(json.dumps(results.result, indent=4))  

Router1
{
    "facts": {
        "uptime": 9600,
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
            "Loopback0"
        ]
    }
}
Router2

...omitted...

Router3

...omitted...

Router4

...omitted...

~~~

However nornir also includes a function for neatly printing the AggregatedResult, this is the print_result() function. This is great for configuration management and backup as it requires little effort to use but is very readable.

~~~python
>>> print_result(task_result)
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
                                 'Loopback0'],
             'model': 'Unknown',
             'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), '
                           'Version 15.4(1)T, DEVELOPMENT TEST SOFTWARE',
             'serial_number': '2048001',
             'uptime': 9600,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router2 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO

...omitted...

^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router3 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO

...omitted...

^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Router4 ** changed : False ***************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO

...omitted...

^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~~~

The above is just a tiny look at all of the awesome things nornir can do on your network!

# Documentation

https://readthedocs.org/projects/nornir/

https://github.com/nornir-automation/nornir