import csv
import re


# interfaceの項目
interface = [
    "device ID", "port", "name", "speed", "duplex", "negotiation", "ip adress", "ip address mask", "untag", "tagged start", "tagged end", "lacp_port"
]
interface_name = []
interface_speed = []
interface_duplex = []

# vlanの項目
vlan = ["device ID", "vlan ID", "name", "ip adress", "ip adress mask"]
vlan_id = []
vlan_name = []

# routingの項目
routing = ["device ID", "dest_ip", "dest_mask", "gw", "metric"]

# 管理情報の項目
Management = ["hostname", "device ID"]

# configを読み込む
with open('config/EX-2_config_set.txt', 'r') as config_txt:
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
            interface = match.group(1)
            description = match.group(2)
            # print(f"Interface: {interface}, Description: {description}")
            continue
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"interfaces \S+ unit (\d+) family \S+ vlan members (.+)$", line)
        # パターンがマッチした場合
        if match:
            unit = match.group(1)
            vlan_members = match.group(2)
            # print(f"Unit: {unit}, Vlan Members: {vlan_members}")
            continue
        # 
        match = re.match(r"speed (\S+)", line)
        if match:
            interface_speed.append(match.group(1))
            continue
        else:
            interface_speed.append('')
    # "routing-instances"で始まる行の処理
    elif line.startswith("routing-options"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"routing-options static route (\S+) next-hop (\S+)", line)
        # パターンがマッチした場合
        if match:
            static_route = match.group(1)
            next_hop = match.group(2)
            # print(f"Destination: {static_route}, Next Hop: {next_hop}")
            continue
    # "vlans"で始まる行の処理
    elif line.startswith("vlans"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r'vlans \S+ description (.*)', line)
        # パターンがマッチした場合
        if match:
            vlan_name.append(match.group(1))
            continue
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"vlans \S+ vlan-id (\d+)", line)
        # パターンがマッチした場合
        if match:
            vlan_id.append(match.group(1))
            continue

print(f'interface_speed : {interface_speed}')

# a = ["vlan_id", "vlan_name"]
# output = './set_to_csv/output.csv'
# with open(output, 'w', newline='') as f:
#     writer = csv.writer(f)
#     list = zip(vlan_id, vlan_name)
#     writer.writerow(a)
#     writer.writerows(list)
