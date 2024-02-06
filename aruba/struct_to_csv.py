import csv
import re
import ipaddress

#------------------------------------------------------
# 関数の定義
#------------------------------------------------------

# リストからCSVに変換する関数
def convertCSV(csv_path, csv_headers, config_lists):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        # リストを1つずつCSVに変換し書き込む
        for config_list in config_lists:
            writer.writerow(config_list)

#------------------------------------------------------
# 変数の定義
#------------------------------------------------------

# outputするCSVファイルのパス
output_directry    = './aruba/output/'
system_csv_path    = output_directry + 'System.csv'
interface_csv_path = output_directry + 'Interface.csv'
routing_csv_path   = output_directry + 'Routing.csv'
vlan_csv_path      = output_directry + 'Vlan.csv'

# 抽出したConfigurationを保存しておくリスト
system_config    = []
interface_config = []
routing_config   = []
vlan_config      = []

# 各configのheaderリスト
system_headers    = ['hostname']
interface_headers = ['port', 'name', 'speed', 'duplex', 'negotiation', 'ip address', 'ip address mask', 'untag', 'tagged start', 'tagged end', 'lacp_port']
routing_headers   = ['dest_ip', 'dest_mask', 'gw', 'metric']
vlan_headers      = ['VlanID', 'name', 'ip address', 'ip address mask']

#------------------------------------------------------
# メインの処理
#------------------------------------------------------

# arubaのconfigを読み込む
with open('./aruba/config/aruba-struct.txt', 'r', newline='') as file:
    # 1行ずつ読み込む
    for line in file:
        # 両端の空白や改行行字を取り除く
        line = line.strip()
        # System (hostname) の抽出
        if line.startswith('hostname'):
            hostname = line.split(' ')[1].replace('"', '')
            system_config.append([hostname])
        # interface の抽出
        elif line.startswith('interface'):
            # interface 内の項目の初期化
            name = port = speed = duplex = negotiation = ip_address = ip_address_mask = untag = tag_start = tag_end = lacp_port = ''
            tag_ranges = []
            # 例：interface 1
            port = line.split(' ')[1]
            while line != 'exit':  # exit が来るまで繰り返す
                # 次の行に行く
                line = next(file).strip()
                if line.startswith('name'):
                    # 例：name "IF-1"
                    # name行の正規表現パターンの定義
                    match = re.match(r'name "(.*?)"', line)
                    # パターンがマッチした場合
                    if match:
                        name = match.group(1)
                        continue
                elif line.startswith('speed-duplex'):
                    # 例：speed-duplex 100-full
                    speed_duplex = line.split(' ')[1]
                    speed  = speed_duplex.split('-')[0]
                    duplex = speed_duplex.split('-')[1]
                elif line.startswith('tagged'):
                    # 例：tagged vlan 92,401-407,409-414,416-424,427
                    tag_ranges = line.split(' ')[2].split(',')
                elif line.startswith('untagged'):
                    # 例：untagged vlan 401
                    untag = line.split(' ')[2]
            if tag_ranges:  # 配列の中身がある場合は
                # tagの範囲の数の分追加（他のconfigは同じ）
                for tag_range in tag_ranges:
                    if '-' in tag_range:  # 409-414 このように tag が範囲を表す場合は
                        tag_start = tag_range.split('-')[0]  # 前半をスタート
                        tag_end   = tag_range.split('-')[1]  # 公判をエンド
                    else:  # 1つだけなら、スタートもエンドも同じ値にする
                        tag_start = tag_end = tag_range
                    # 抽出した config をリスト化して追加
                    interface_config.append([name, port, speed, duplex, negotiation, ip_address, ip_address_mask, untag, tag_start, tag_end, lacp_port])
            else:  # ない場合はそのまま追加
                interface_config.append([name, port, speed, duplex, negotiation, ip_address, ip_address_mask, untag, tag_start, tag_end, lacp_port])
        elif line.startswith('vlan'):  # vlan で始まるなら
            # 例：vlan 1
            # 各項目の初期化
            vlan_id = name = ip_address = ip_address_mask = ''
            vlan_id = line.split(' ')[1]
            while line != 'exit':  # exit が来るまで繰り返す
                # 次の行に行く
                line = next(file).strip()
                if line.startswith('name'):
                    # 例：name "DEFAULT_VLAN"
                     # name行の正規表現パターンの定義
                    match = re.search(r'name "(.*?)"', line)
                    # パターンがマッチした場合
                    if match:
                        name = match.group(1)
                        continue
                elif line.startswith('ip address'):
                    # 例：ip address 192.168.66.88 255.255.255.0
                    # IPアドレスとサブネットマスクを取得
                    ip_address, subnet_mask = line.split()[2], line.split()[3]
                    # IPv4アドレスオブジェクトを作成
                    address_obj = ipaddress.IPv4Address(ip_address)
                    # IPv4ネットワークオブジェクトを作成
                    network_obj = ipaddress.IPv4Network(f'{address_obj}/{subnet_mask}', strict=False)
                    # プレフィックス長を取得
                    ip_address_mask = network_obj.prefixlen

            # 抽出した config をリスト化して追加
            vlan_config.append([vlan_id, name ,ip_address, ip_address_mask])
        elif line.startswith('ip route'):
            # 例：ip route 10.6.1.0 255.255.255.0 10.5.16.250
            dest_ip = dest_mask = gateway = metric = ''
            dest_ip   = line.split(' ')[2]
            dest_mask = line.split(' ')[3]
            gateway   = line.split(' ')[4]
            dest_mask = '24' if dest_mask == '255.255.255.0' else dest_mask
            # 抽出した config をリスト化して追加
            routing_config.append([dest_ip, dest_mask, gateway, metric])


# 抽出した各Configuration をCSVに変換する
convertCSV(system_csv_path, system_headers, system_config)           # System
convertCSV(interface_csv_path, interface_headers, interface_config)  # Interface
convertCSV(vlan_csv_path, vlan_headers, vlan_config)                 # Vlan
convertCSV(routing_csv_path, routing_headers, routing_config)        # Routing
