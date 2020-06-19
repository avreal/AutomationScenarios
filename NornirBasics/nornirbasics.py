from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import json

nr = InitNornir(config_file="./config.yaml")
task_result = nr.run(task=napalm_get,getters=["facts"])


print("This script is empty because I am simply running this with -i to examine task_result in the interpreter")