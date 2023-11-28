import re

# configを読み込む
with open('config/HP_config_short.txt', 'r') as config_txt:
    # 各行を配列linesに格納
    lines = config_txt.readlines()

for line in lines:
    # "sntp server"で始まる行の処理
    if line.startswith("sntp server"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"sntp server priority (\d+) (\S+)$", line)
        # パターンがマッチした場合
        if match:
            priority = match.group(1)
            sntp_server = match.group(2)
            print(f"Priority: {priority}, SNTP Server: {sntp_server}")
            continue
    # "ip route"で始まる行の処理
    elif line.startswith("ip route"):
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"ip route (\S+) (\S+) (\S+)$", line)
        # パターンがマッチした場合
        if match:
            destination = match.group(1)
            subnet_mask = match.group(2)
            next_hop    = match.group(3)
            print(f"Destination: {destination}, Subnet Mask: {subnet_mask}, Next Hop: {next_hop}")
            continue
    # "interface"で始まる行の処理
    elif line.startswith("interface"):
        number = line.split()[1]
        # パターンマッチングのための正規表現パターンの定義
        match = re.match(r"routing-instances mgmt_junos routing-options static route (\S+) next-hop (\S+)", line)
        # パターンがマッチした場合
        if match:
            static_route = match.group(1)
            next_hop = match.group(2)
            print(f"Destination: {static_route}, Next Hop: {next_hop}")
            continue
    # "snmp-server"で始まる行の処理
	# 後回し
    # elif line.startswith("snmp-server"):
    #     # パターンマッチングのための正規表現パターンの定義
    #     match = re.match(r"snmp-server community "SNMP-COM1" operator unrestricted", line)
    #     # パターンがマッチした場合
    #     if match:
    #         static_route = match.group(1)
    #         next_hop = match.group(2)
    #         print(f"Destination: {static_route}, Next Hop: {next_hop}")
    #         continue
    # "vlan"で始まる行の処理
    elif line.startswith("vlan"):
        print(line)
        # # パターンマッチングのための正規表現パターンの定義
        # match = re.match(r'vlans (\S+) description "(.*)"', line)
        # # パターンがマッチした場合
        # if match:
        #     name = match.group(1)
        #     description = match.group(2)
        #     print(f"Name: {name}, Description: {description}")
        #     continue
        # # パターンマッチングのための正規表現パターンの定義
        # match = re.match(r"vlans \S+ vlan-id (\d+)", line)
        # # パターンがマッチした場合
        # if match:
        #     vlan_id = match.group(1)
        #     print(f"Vlan ID: {vlan_id}")
        continue