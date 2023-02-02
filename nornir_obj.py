'''
Python3 Nornir Script
'''
#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.inventory import ConnectionOptions
from nornir.core.filter import F
import pprint # Required to Pretty Print results
pp = pprint.PrettyPrinter(indent=4) # Pretty Printer Config
import ipdb

print('\n**********************')
print('\n*** YAML Inventory ***')
print('\n**********************')

# Initialise Nornir
nr = InitNornir(config_file='config.yaml')

# Credentials
nr.inventory.defaults.username = input('Username: ')
nr.inventory.defaults.password = input('Password: ')

# Simple Filter
nornir_obj = nr.filter(F(groups__contains='DEV'))
print('\nNornir Inventory Hosts: ' + str(nornir_obj.inventory.hosts))
print('\nNornir Inventory Username: ' + str(nornir_obj.inventory.defaults.username))
print('\nNornir Inventory Password: ' + str(nornir_obj.inventory.defaults.password))

# Loop through each host in our inventory and print the data
for host in nornir_obj.inventory.hosts:
    print('\nNornir Inventory ' + host + ' Data: ' + str(nornir_obj.inventory.hosts[host].data))

# Slightly more complex filter. I'll not do anything with this, just demo
# how to filter on additional values.
nornir_obj_complex = nr.filter(F(groups__contains='DEV') & \
    (F(os='ios')))

ipdb.set_trace()
print('\nPress c to continue or n to step through')
print('\n****************************')
print('*** Nornir/ NetMiko Task ***')
print('****************************')
print('Please wait...')


from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

task_a = nornir_obj.run(task=netmiko_send_command, command_string='show ip route', use_textfsm=True)
print('\nNetMiko Task Type: ' + str(type(task_a)))
print_result(task_a)

dict_a = {}

for host, response in task_a.items():
    # host = hostname
    # response = MultiResult: [Result: "netmiko_send_command"]
    dict_a[host] = response.result

ipdb.set_trace()
print('\nPress c to continue or n to step through')
print('\n****************************')
print('\n*** Template-Text-Parser ***')
print('\n****************************')
print('Please wait...')

from ttp import ttp # Template Text Parser
import json

nornir_obj = nr.filter(F(groups__contains='DEV')) # Reinitialise Nornir just in case.
task_b = nornir_obj.run(task=netmiko_send_command, command_string='show run')

dict_b = {}

for host, response in task_b.items():
    parser = ttp(data=response.result, template='cisco_nxos.ttp')
    # Define the Parse with the data= and template=
    # A majority of my hosts are Nexus5000, so I'm using the cisco_nxos.ttp template.
    # You could use if conditions to parse the response against the appropriate
    # template.
    parser.parse() # Parse the data
    parsed = parser.result(format='json')[0] # Use [0] to drop '\n'
    json_obj = json.loads(parsed) # Render parsed into a JSON structure
    dict_b[host] = json_obj[0] # json_obj is a dict with a list [{}]

pp.pprint(dict_b)

ipdb.set_trace()
print('\n***********')
print('\n*** EOF ***')
print('\n***********')
