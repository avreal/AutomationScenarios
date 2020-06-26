from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import json

nr = InitNornir(config_file="./config.yaml")
task_result = nr.run(task=netmiko_send_command, command_string="show ip ospf database")


print("This script is empty because I am simply running this with -i to examine task_result in the interpreter")