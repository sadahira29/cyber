import os
import csv
import xml.etree.ElementTree as ET
import sys

#======================================================
# グローバル変数の定義
#======================================================
# コマンドライン引数
device_id = sys.argv[1]
juniper_config_xml = sys.argv[2]
output_directry    = sys.argv[3]

# 出力するCSVファイルのパス
system_csv_path    = output_directry + '/System.csv'
interface_csv_path = output_directry + '/Interface.csv'
routing_csv_path   = output_directry + '/Routing.csv'
vlan_csv_path      = output_directry + '/Vlan.csv'

# 抽出した config を保存しておくリスト
system_config    = []   # System
interface_config = []   # Interface
routing_config   = []   # Routing
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
    'ip_address',       # IPアドレス
    'ip_address_mask',  # IPアドレスのサブネットマスク
    'untag',            # VLANなしの場合の設定
    'tagged_start',     # タギングの開始VLAN
    'tagged_end',       # タギングの終了VLAN
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
    'ip_address',       # VLANのIPアドレス
    'ip_address_mask'   # VLANのIPアドレスのサブネットマスク
]

#======================================================
# 関数の定義
#======================================================

# System(管理情報)の config を抽出する関数
def extract_system_config(root):
    global system_config
    hostname = ''
    # XPathでhost-nameタグを検索
    hostname_tag = root.find(".//system/host-name")
    if hostname_tag is not None:
        hostname = hostname_tag.text
        # 抽出した config をヘッダーの順番に合わせてリスト化して追加
        system_config.append([hostname, device_id])

# Interfaceの config 抽出する関数
def extract_interface_config(root):
    global interface_config
    # XPathでinterfacesタグを検索
    XPath = './/interfaces/interface'
    # 子ノードのinterfaceタグをすべて取得
    interfaces = root.findall(XPath)
    # interfaceタグ内の必要な設定を抽出して１つのリストに格納し、
    # そのリストを1つずつinterface_configに格納する
    for interface in interfaces:
        # 各変数の初期化（ループするたびに初期化する）
        name = port = speed = duplex = negotiation = ip_address = subnet_mask = untag = tag_start = tag_end = lacp_port = ''
        # 複数タグを保存するリスト
        vlan_tags = []

        # interface名からポート番号を抽出
        interface_name = interface.find('name').text.split('/')
        interface_type = interface_name[0]
        if interface_type.startswith('ge'):
            # juniperではポート番号から０から始まるので
            # arubaに合わせるために＋１している
            port = int(interface_name[2]) + 1
        else:  # me0 はとりあえず無視している
            continue

        # description の抽出
        description_tag = interface.find('description')
        # is not Noneを書かないと指定したタグがない時にエラーになる
        if description_tag is not None:
            name = description_tag.text
        # スピードの抽出
        speed_tag = interface.find('ether-options/speed')
        if speed_tag is not None:
            speed  = speed_tag[0].tag.split('-')[1]
            duplex = 'full'  # full であると仮定
        # tag, untagの抽出（推測）
        switching_tag = interface.find('.//ethernet-switching')
        if switching_tag is not None:
            vlans = root.findall('.//vlans/vlan')
            port_mode = switching_tag[0].text
            # port_modeが'access'のとき，untagを取得
            if port_mode == 'access':
                member_name = switching_tag.find('vlan/members')
                untag = get_vlan_id(member_name, vlans)
            # port_modeが'access'のとき，untagを取得
            elif port_mode == 'trunk':
                member_names = switching_tag.findall('vlan/members')
                # メンバ(vlan名)に対するvlan idを取得する
                for member_name in member_names:
                    vlan_tags.append(get_vlan_id(member_name, vlans))
        # ip adressの抽出（仮定）
        address_tag = interface.find('.//inet/address')
        if address_tag is not None:
            # CIDR表記のIPアドレスを'/'で宛先アドレスとマスクに分ける
            ip_adress_cidr = address_tag.find('name').text.split('/')
            ip_address = ip_adress_cidr[0]
            subnet_mask = ip_adress_cidr[1]
        # tagの割り当てと interface_config への格納
        if vlan_tags:
            for vlan_tag in vlan_tags:
                # 開始タグと終了タグの設定
                tag_start = tag_end = vlan_tag
                # 抽出した config をヘッダーの順番に合わせてリスト化して追加
                interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, subnet_mask, untag, tag_start, tag_end, lacp_port])
        else:
            # 抽出した config をヘッダーの順番に合わせてリスト化して追加
            interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, subnet_mask, untag, tag_start, tag_end, lacp_port])

# Routing の config 抽出する関数
def extract_routing_config(root):
    global routing_config
    # routeタグの子ノードをすべて抽出
    XPath = './/routing-options/static/route'
    routes = root.findall(XPath)
    for route in routes:
        # 各変数の初期化（ループするたびに初期化する）
        dest_ip = dest_mask = gateway = metric = ''
        # CIDR表記のIPアドレスを'/'で宛先アドレスとマスクに分ける
        ip_adress_cidr = route.find('name').text.split('/')
        dest_ip = ip_adress_cidr[0]
        dest_mask = ip_adress_cidr[1]
        gateway = route.find('next-hop').text
        # 抽出した config をヘッダーの順番に合わせてリスト化して追加
        routing_config.append([device_id, dest_ip, dest_mask, gateway, metric])

# Vlan の config 抽出する関数
def extract_vlan_config(root):
    # vlanタグの子ノードをすべて抽出
    XPath = './/vlans/vlan'
    vlans = root.findall(XPath)
    for vlan in vlans:
        # 各変数の初期化（ループするたびに初期化する）
        vlan_id = vlan_desc = ip_address = subnet_mask = ''
        vlan_id   = vlan.find('vlan-id').text
        vlan_desc = vlan.find('description').text
        # 抽出した config をヘッダーの順番に合わせてリスト化して追加
        vlan_config.append([device_id, vlan_id, vlan_desc, ip_address, subnet_mask])

# メンバ名（vlan名）と一致するvlan idを取得する関数
def get_vlan_id(member_name, vlans):
    for vlan in vlans:
        vlan_name = vlan.find('name')
        # メンバとvlan名が一致した時idの取得
        if  member_name.text == vlan_name.text:
            return vlan.find('vlan-id').text

# リストからCSVに変換する関数
def list_to_csv(csv_path, csv_headers, config_lists):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        # リストを1つずつCSVに変換し書き込む
        for config_list in config_lists:
            writer.writerow(config_list)

# メイン関数
def main():
    # グローバル変数の宣言
    global device_id, juniper_config_xml

    # XMLを扱えるようにするための準備
    tree = ET.parse(juniper_config_xml)
    root = tree.getroot()

    # 各項目の config の抽出
    extract_system_config(root)     # System(管理情報)
    extract_interface_config(root)  # Interface
    extract_routing_config(root)    # Routing
    extract_vlan_config(root)       # Vlan

    # 抽出した  config  リストをCSVに変換し出力する
    list_to_csv(system_csv_path, system_headers, system_config)           # System(管理情報)
    list_to_csv(interface_csv_path, interface_headers, interface_config)  # Interface
    list_to_csv(routing_csv_path, routing_headers, routing_config)        # Routing
    list_to_csv(vlan_csv_path, vlan_headers, vlan_config)                 # Vlan

#======================================================
# プログラムの起点
#======================================================

if __name__ == '__main__':
    main()
