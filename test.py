import csv
import re

# 入力文字列
# configを読み込む
with open('config/juniper_config.txt', 'r') as config_txt:
	# 各行を配列linesに格納
	lines = config_txt.readlines()

interfaces = []
description = []
unit = []
family = []
vlan_members = []

for line in lines:
    line = line.lstrip("set").strip()
    if line.startswith("interfaces"):
        print(line)
        match = re.match(r"interfaces (\S+) description (.+)$", line)
        if match:
            interfaces.append(match.group(1))
            description.append(match.group(2))
            print(match.group(1))
            print(match.group(2))
            continue
        match = re.match(r"interfaces \S+ unit (\d+) family (\S+) vlan members (.+)$", line)
        if match:
            unit.append(match.group(1))
            family.append(match.group(2))
            vlan_members.append(match.group(3))
            print(match.group(1))
            print(match.group(2))
            print(match.group(3))
            continue