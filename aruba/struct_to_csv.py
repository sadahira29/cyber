import csv
import re
import os
import ipaddress

#======================================================
# 変数の定義
#======================================================

# outputするCSVファイルのパス
output_directry    = './output/'
system_csv_path    = output_directry + 'System_ar.csv'
interface_csv_path = output_directry + 'Interface_ar.csv'
routing_csv_path   = output_directry + 'Routing_ar.csv'
vlan_csv_path      = output_directry + 'Vlan_ar.csv'

# 抽出した config を保存しておくリスト
system_config    = []   # システム
interface_config = []   # インターフェース
routing_config   = []   # ルーティング
vlan_config      = []   # VLAN

# システム情報のヘッダ
system_headers    = [
    'hostname',         # ホスト名
    'deviceID'          # 機器ID（識別子）
]
# インターフェース情報のヘッダ
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
# ルーティング情報のヘッダ
routing_headers = [
    'deviceID',         # 機器ID
    'dest_ip',          # 宛先IPアドレス
    'dest_mask',        # 宛先サブネットマスク
    'gw',               # ゲートウェイ
    'metric'            # メトリック
]
# VLAN情報のヘッダ
vlan_headers = [
    'deviceID',         # 機器ID
    'VlanID',           # VLAN ID
    'name',             # VLANの名前
    'ip address',       # VLANのIPアドレス
    'ip address mask'   # VLANのIPアドレスのサブネットマスク
]

#======================================================
# 関数の定義
#======================================================

# 機器IDを取得する関数
def get_device_id():
    # 入力された機器IDを取得
    device_id = input('Enter a device ID: ')
    # バリデーションチェック
    while True:
        if not device_id:  # 未入力の場合
            print("Error: Device ID cannot be empty.")
        else:
            # 正規表現パターンを定義(半角英数字，ハイフン，アンダースコアのみを有効)
            pattern = re.compile("^[a-zA-Z0-9_-]+$")
            # 入力文字列がパターンに一致するか確認
            if pattern.match(device_id):
                break
            else:
                print("Error: Device ID can only contain alphanumeric characters, hyphens, and underscores. ")
        device_id = input('Please enter a valid device ID again: ')
    return device_id

# ファイル名を取得する関数
def get_aruba_conf():
    file_name = input("Enter the file name or path of aruba config: ")
    while True:
        if os.path.exists(file_name):  # ファイルが存在するなら
            break
        else:  # 存在しないならもう一度入力させる
            print(f'No such file or directory: "{file_name}"')
            file_name = input("Enter the correct file name or path of aruba config: ")
    return file_name

# リストからCSVに変換する関数
def list_to_csv(csv_path, csv_headers, config_lists):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        # リストを1つずつCSVに変換し書き込む
        for config_list in config_lists:
            writer.writerow(config_list)

# サブネットマスクをプレフィックス長に変換する関数
def get_prefix_len(ip_address, subnet_mask):
    # IPv4アドレスオブジェクトを作成
    address_obj = ipaddress.IPv4Address(ip_address)
    # IPv4ネットワークオブジェクトを作成
    network_obj = ipaddress.IPv4Network(f'{address_obj}/{subnet_mask}', strict=False)
    # プレフィックス長を取得
    prefix_len = network_obj.prefixlen
    # プレフィックス長を返す
    return prefix_len

def main():
    # コマンドライン引数から機器IDを取得
    device_id = get_device_id()
    # 変換対象のaruba configのファイル名（パス）を取得
    aruba_config = get_aruba_conf()
    # arubaのconfigを読み込む
    with open(aruba_config, 'r', newline='', encoding="utf-8") as file:
        # 1行ずつ読み込む
        for line in file:
            # 両端の空白や改行行字を取り除く
            line = line.strip()
            # System  の config(hostname) 抽出
            if line.startswith('hostname'):
                hostname = line.split()[1].replace('"', '')
                # 抽出した config をヘッダの順番に合わせてリスト化して追加
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
                        # 抽出した config をヘッダの順番に合わせてリスト化して追加
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
                        prefix_len  = get_prefix_len(ip_address, subnet_mask)  # プレフィックス長
                # 抽出した config をヘッダの順番に合わせてリスト化して追加
                vlan_config.append([device_id, vlan_id, vlan_name ,ip_address, prefix_len])
            # routing の config 抽出
            elif line.startswith('ip route'):  # 例：ip route 10.6.1.0 255.255.255.0 10.5.16.250
                # 各項目の初期化
                dest_ip = dest_mask = prefix_len = gateway = metric = ''
                dest_ip    = line.split()[2]  # IPアドレス
                dest_mask  = line.split()[3]  # サブネットマスク
                gateway    = line.split()[4]  # ゲートウェイ
                prefix_len = get_prefix_len(dest_ip, dest_mask)  # プレフィックス長
                # 抽出した config をヘッダの順番に合わせてリスト化して追加
                routing_config.append([device_id, dest_ip, prefix_len, gateway, metric])

    # 抽出した各Configuration をCSVに変換する
    list_to_csv(system_csv_path, system_headers, system_config)           # System
    list_to_csv(interface_csv_path, interface_headers, interface_config)  # Interface
    list_to_csv(vlan_csv_path, vlan_headers, vlan_config)                 # Vlan
    list_to_csv(routing_csv_path, routing_headers, routing_config)        # Routing

#======================================================
# プログラムの起点
#======================================================
if __name__ == '__main__':
    main()
