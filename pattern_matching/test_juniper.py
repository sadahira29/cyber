import csv
import re

# configを読み込む
with open('config/juniper_config_short.txt', 'r') as config_txt:
    # 各行を配列linesに格納
    lines = config_txt.readlines()

for line in lines:
    # 文頭の "set" を削除して余分な空白を取り除く
    line = line.lstrip("set").strip()
    # print(line)
    # "interface"で始まる行の処理
    if line.startswith("interfaces"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"interfaces (\S+) description (.+)$", line)
        # パターンがマッチした場合
        if match:
            interfaces = match.group(1)
            description = match.group(2)
            print(f"Interfaces: {interfaces}, Description: {description}")
            continue
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"interfaces \S+ unit (\d+) family \S+ vlan members (.+)$", line)
        # パターンがマッチした場合
        if match:
            unit = match.group(1)
            vlan_members = match.group(2)
            print(f"Unit: {unit}, Vlan Members: {vlan_members}")
            continue
    # "snmp"で始まる行の処理
    # elif line.startswith("snmp"): # 後回し
    #     # パターンマッチングのための正規表現パターンの定義
    #     match = re.match(r"snmp (\S+) location (\S+)$", line)
    #     # パターンがマッチした場合
    #     if match:
    #         continue
    # "routing-instances"で始まる行の処理
    elif line.startswith("routing-instances"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"routing-instances mgmt_junos routing-options static route (\S+) next-hop (\S+)", line)
        # パターンがマッチした場合
        if match:
            static_route = match.group(1)
            next_hop = match.group(2)
            print(f"Destination: {static_route}, Next Hop: {next_hop}")
            continue
    # "vlans"で始まる行の処理
    elif line.startswith("vlans"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r'vlans (\S+) description "(.*)"', line)
        # パターンがマッチした場合
        if match:
            name = match.group(1)
            description = match.group(2)
            print(f"Name: {name}, Description: {description}")
            continue
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"vlans \S+ vlan-id (\d+)", line)
        # パターンがマッチした場合
        if match:
            vlan_id = match.group(1)
            print(f"Vlan ID: {vlan_id}")
            continue