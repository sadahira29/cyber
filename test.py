import csv
import re

# configを読み込む
with open('config/juniper_config_short.txt', 'r') as config_txt:
	# 各行を配列linesに格納
	lines = config_txt.readlines()


for line in lines:
    line = line.lstrip("set").strip()
    if line.startswith("interfaces"):
        print(line)
        match = re.match(r"interfaces (\S+) description (.+)$", line)
        if match:
            interfaces = match.group(1)
            description = match.group(2)
            print(f"Interfaces: {interfaces}, Description: {description}")
            continue
        match = re.match(r"interfaces \S+ unit (\d+) family (\S+) vlan members (.+)$", line)
        if match:
            unit = match.group(1)
            family = match.group(2)
            vlan_members = match.group(3)
            print(f"Unit: {unit}, Family: {family}, Vlan Members: {vlan_members}")
            continue
    elif line.startswith("snmp"): # 後回し
        print(line)
        # match = re.match(r"snmp (\S+) description (.+)$", line)
        # if match:
        continue
    elif line.startswith("routing-instances"):
        print(line)
        match = re.match(r"routing-instances mgmt_junos routing-options static route (\S+) next-hop (\S+)", line)
        if match:
            static_route = match.group(1)
            next_hop = match.group(2)
            print(f"Destination: {static_route}, Next Hop: {next_hop}")
            continue
    elif line.startswith("vlans"):
        print(line)
        match = re.match(r'vlans (\S+) description "(.*)"', line)
        if match:
            name = match.group(1)
            description = match.group(2)
            print(f"Name: {name}, Description: {description}")
            continue
        match = re.match(r"vlans \S+ vlan-id (\d+)", line)
        if match:
            vlan_id = match.group(1)
            print(f"Vlan ID: {vlan_id}")
            continue