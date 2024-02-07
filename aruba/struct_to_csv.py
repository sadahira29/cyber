import csv
import re
import ipaddress
import sys

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

# サブネットマスクをプレフィックス長に変換する関数
def getPrefixLen(ip_address, subnet_mask):
    # IPv4アドレスオブジェクトを作成
    address_obj = ipaddress.IPv4Address(ip_address)
    # IPv4ネットワークオブジェクトを作成
    network_obj = ipaddress.IPv4Network(f'{address_obj}/{subnet_mask}', strict=False)
    # プレフィックス長を取得
    prefix_len = network_obj.prefixlen
    # プレフィックス長を返す
    return prefix_len

#------------------------------------------------------
# 変数の定義
#------------------------------------------------------

# outputするCSVファイルのパス
output_directry    = './output/'
system_csv_path    = output_directry + 'System.csv'
interface_csv_path = output_directry + 'Interface.csv'
routing_csv_path   = output_directry + 'Routing.csv'
vlan_csv_path      = output_directry + 'Vlan.csv'

# 抽出した config を保存しておくリスト
system_config    = []   # システム
interface_config = []   # インターフェース
routing_config   = []   # ルーティング
vlan_config      = []   # VLAN

# システム情報のヘッダー
system_headers    = [
    'hostname',         # ホスト名
    'deviceID'          # 機器ID（識別子）
]
# インターフェース情報のヘッダー
interface_headers = [
    'deviceID',         # 機器ID
    'port',             # ポート番号
    'name',             # インターフェースの名前
    'speed',            # 通信速度
    'duplex',           # デュプレックスモード
    'negotiation',      # ネゴシエーション設定
    'ip address',       # IPアドレス
    'ip address mask',  # IPアドレスのサブネットマスク
    'untag',            # VLANなしの場合の設定
    'tagged start',     # タギングの開始VLAN
    'tagged end',       # タギングの終了VLAN
    'lacp_port'         # LACP（Link Aggregation Control Protocol）ポートの設定
]
# ルーティング情報のヘッダー
routing_headers = [
    'deviceID',         # 機器ID
    'dest_ip',          # 宛先IPアドレス
    'dest_mask',        # 宛先サブネットマスク
    'gw',               # ゲートウェイ
    'metric'            # メトリック
]
# VLAN情報のヘッダー
vlan_headers = [
    'deviceID',         # 機器ID
    'VlanID',           # VLAN ID
    'name',             # VLANの名前
    'ip address',       # VLANのIPアドレス
    'ip address mask'   # VLANのIPアドレスのサブネットマスク
]

#------------------------------------------------------
# メインの処理
#------------------------------------------------------
if __name__ == '__main__':
    # コマンドライン引数として機器IDを取得
    device_id = input('Enter the decice ID: ')
    # arubaのconfigを読み込む
    with open('./config/aruba-struct.txt', 'r', newline='') as file:
        # 1行ずつ読み込む
        for line in file:
            # 両端の空白や改行行字を取り除く
            line = line.strip()
            # System  の config(hostname) 抽出
            if line.startswith('hostname'):
                hostname = line.split()[1].replace('"', '')
                system_config.append([hostname, device_id])
            # interface の config 抽出
            elif line.startswith('interface'):  # 例：interface 1
                # interface 内の項目の初期化
                name = port = speed = duplex = negotiation = ip_address = subnet_mask = prefix_len = untag = tag_start = tag_end = lacp_port = ''
                # 複数のtagを格納するためのリスト
                tag_ranges = []
                # ポートの抽出
                port = line.split()[1]
                while line != 'exit':  # exit が来るまで繰り返す
                    # 次の行に行く
                    line = next(file).strip()
                    if line.startswith('name'):
                        # 例：name "IF-1"
                        # name行の正規表現の定義
                        name = re.search(r'name "(.*?)"', line).group(1)
                    elif line.startswith('speed-duplex'):
                        # 例：speed-duplex 100-full
                        speed_duplex = line.split()[1]
                        # 例：100-full
                        speed  = speed_duplex.split('-')[0]
                        duplex = speed_duplex.split('-')[1]
                    elif line.startswith('untagged'):
                        # 例：untagged vlan 401
                        untag = line.split()[2]
                    elif line.startswith('tagged'):
                        # 例：tagged vlan 92,401-407,409-414,416-424,427
                        tag_ranges = line.split()[2].split(',')
                if tag_ranges:  # tag_ranges の中身がある場合は
                    # tagの範囲の数の分追加（他の config は同じ）
                    for tag_range in tag_ranges:
                        if '-' in tag_range:  # 409-414 このように tag が範囲を表す場合は
                            tag_start = tag_range.split('-')[0]  # 前半をスタート
                            tag_end   = tag_range.split('-')[1]  # 後半をエンド
                        else:  # 1つだけなら、スタートもエンドも同じ値にする
                            tag_start = tag_end = tag_range
                        # 抽出した config をヘッダーに合わせた順番にリスト化して追加
                        interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, prefix_len, untag, tag_start, tag_end, lacp_port])
                else:  # ない場合はそのまま追加
                    interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, prefix_len, untag, tag_start, tag_end, lacp_port])
            # vlan の config 抽出
            elif line.startswith('vlan'):  # 例：vlan 1
                # 各項目の初期化
                vlan_id = vlan_name = ip_address = subnet_mask = prefix_len = ''
                # vlanIDの抽出
                vlan_id = line.split()[1]
                while line != 'exit':  # exit が来るまで繰り返す
                    # 次の行に行く
                    line = next(file).strip()
                    if line.startswith('name'):  # 例：name "DEFAULT_VLAN"
                        # name行の正規表現パターンの定義
                        match = re.search(r'name "(.*?)"', line)
                        # パターンがマッチした場合
                        if match:
                            vlan_name = match.group(1)
                    # IPアドレスとサブネットマスク（プレフィックス長）の抽出
                    elif line.startswith('ip address'):  # 例：ip address 192.168.66.88 255.255.255.0
                        ip_address  = line.split()[2]  # IPアドレス
                        subnet_mask = line.split()[3]  # サブネットマスク
                        prefix_len  = getPrefixLen(ip_address, subnet_mask)  # プレフィックス長
                # 抽出した config をヘッダーに合わせた順番にリスト化して追加
                vlan_config.append([device_id, vlan_id, vlan_name ,ip_address, prefix_len])
            # routing の config 抽出
            elif line.startswith('ip route'):  # 例：ip route 10.6.1.0 255.255.255.0 10.5.16.250
                # 各項目の初期化
                ip_address = subnet_mask = prefix_len = gateway = metric = ''
                ip_address  = line.split()[2]  # IPアドレス
                subnet_mask = line.split()[3]  # サブネットマスク
                gateway     = line.split()[4]  # ゲートウェイ
                prefix_len  = getPrefixLen(ip_address, subnet_mask)  # プレフィックス長
                # 抽出した config をヘッダーに合わせた順番にリスト化して追加
                routing_config.append([device_id, ip_address, prefix_len, gateway, metric])

    # 抽出した各Configuration をCSVに変換する
    convertCSV(system_csv_path, system_headers, system_config)           # System
    convertCSV(interface_csv_path, interface_headers, interface_config)  # Interface
    convertCSV(vlan_csv_path, vlan_headers, vlan_config)                 # Vlan
    convertCSV(routing_csv_path, routing_headers, routing_config)        # Routing
