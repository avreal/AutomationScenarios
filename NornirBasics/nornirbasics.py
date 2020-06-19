#

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import json

nr = InitNornir(config_file="./config.yaml")
task_result = nr.run(task=napalm_get,getters=["facts"])


print("First lets look at the type of the result object with type(task_result): ", type(task_result), '\n')


print("Then the output of print(task_result): ", task_result)
print("*" * 150)

print("We can access the MultiResult objects within the AggregatedResult by using the hostnames as the key, here I will do type(task_result['Router1']): ", type(task_result['Router1']))

print("\nLets look at the output of print(task_result['Router1']): ", task_result['Router1'])


print("*" * 150)

print("We can unpack the Multiresult object with the .result method, lets do type(task_result['Router1'].result):  ", type(task_result['Router1'].result), '\n')

print("Now the output of print(result.task_result): ", task_result['Router1'].result)

print("*" * 150)

print("Now we have visibility into the dictionaries that make up the output of the nornir task that we ran, we can construct a simple loop to display all of the Hostnames and their associated dictionaries in a neat fashion: \n")

for x in task_result:
    print(type(x))
    print(x)
    for k in task_result[x]:
        print(type(k.result))
        print(k.result)

print("We can clean this up a bit with json.dumps")

for x in task_result:
    print(x)
    for k in task_result[x]:
        print(json.dumps(k.result, indent=4))  

print("\nHowever nornir comes with a print_result function that we can use on our original task_result, which saves us the trouble of accessing the data ourselves, unless we need the underlying data for some other logic. Here is the output of print_result(task_result): \n")

print_result(task_result)

