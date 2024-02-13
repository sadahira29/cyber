import csv
import xml.etree.ElementTree as ET


#------------------------------------------------------
# 関数の定義
#------------------------------------------------------

# リストからCSVに変換する関数
def export_list_to_csv(csv_path, csv_headers, config_lists):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        # リストを1つずつCSVに変換し書き込む
        for config_list in config_lists:
            writer.writerow(config_list)

def get_vlan_id(member_name, vlans):
    for vlan in vlans:
        vlan_name = vlan.find('name').text
        # メンバとvlan名が一致した時idの取得
        if  member_name.text == vlan_name:
            return vlan.find('vlan-id').text

#------------------------------------------------------
# 変数の定義
#------------------------------------------------------

# outputするCSVファイルのパス
output_directry    = './output/'
system_csv_path    = output_directry + 'System_ju.csv'
interface_csv_path = output_directry + 'Interface_ju.csv'
routing_csv_path   = output_directry + 'Routing_ju.csv'
vlan_csv_path      = output_directry + 'Vlan_ju.csv'

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
    # 変換対象のaruba configのファイル名（パス）を取得
    juniper_config_xml = input("Enter the file name or path of juniper config(XML): ")
    # XMLを扱えるようにするための準備
    tree = ET.parse(juniper_config_xml)
    root = tree.getroot()

    # System(管理情報)のConfiguration抽出
    # 指定したXPathに対応する子ノードの抽出
    system_hostname = root.find(".//system/host-name")
    if system_hostname is not None:
        hostname = system_hostname.text
        # 抽出した config をヘッダーの順番に合わせてリスト化して追加
        system_config.append([hostname, device_id])
    # InterfaceのConfiguration抽出
    # XML例：
        # <interface>
        #     <name>ge-0/0/20</name>
        #     <description>IF-21</description>
        #     <ether-options>
        #         <speed>
        #             <ethernet-100m/>
        #         </speed>
        #     </ether-options>
        #     <unit>
        #         <name>0</name>
        #         <family>
        #             <ethernet-switching>
        #                 <port-mode>access</port-mode>
        #                 <vlan>
        #                     <members>vlan421</members>
        #                 </vlan>
        #             </ethernet-switching>
        #         </family>
        #     </unit>
        # </interface>
    # 指定したXPathに対応する子ノードの抽出
    XPath = './/interfaces/interface'
    # interfaceタグの子ノードをすべて抽出
    interfaces = root.findall(XPath)
    for interface in interfaces:
        # 各変数の初期化（ループするたびに初期化する）
        name = port = speed = duplex = negotiation = ip_address = subnet_mask = untag = tag_start = tag_end = lacp_port = ''
        vlan_tags = []

        # interfaceのタイプからポート番号を抽出
        current_tag = interface.find('name').text.split('/')
        interface_type = current_tag[0]
        if interface_type.startswith('ge'):
            # juniperではポート番号から０から始まるので
            # arubaに合わせるために＋１している
            port = int(current_tag[2]) + 1
        else:  # me0 はとりあえず無視している
            continue
        # description の抽出
        current_tag = interface.find('description')
        # is not Noneを書かないと指定したタグがない時にエラーになる
        if current_tag is not None:
            name = current_tag.text
        # スピードの抽出
        current_tag = interface.find('ether-options/speed')
        if current_tag is not None:
            speed  = current_tag[0].tag.split('-')[1]
            duplex = 'full'  # full であると仮定
        # tag, untagの抽出（推測）
        current_tag = interface.find('.//ethernet-switching')
        if current_tag is not None:
            vlans = root.findall('.//vlans/vlan')
            port_mode = current_tag[0].text
            # port_modeが'access'のとき，untagを取得
            if port_mode == 'access':
                member_name = current_tag.find('vlan/members')
                untag = get_vlan_id(member_name, vlans)
            # port_modeが'access'のとき，untagを取得
            elif port_mode == 'trunk':
                member_names = current_tag.findall('vlan/members')
                # メンバ(vlan名)に対するvlan idを取得する
                for member_name in member_names:
                    vlan_tags.append(get_vlan_id(member_name, vlans))
        # ip adressの抽出（仮定）
        current_tag = interface.find('.//inet/address')
        if current_tag is not None:
            ip_adress_cidr = current_tag.find('name').text.split('/')
            ip_address = ip_adress_cidr[0]
            subnet_mask = ip_adress_cidr[1]
        # tagの割り当て
        if vlan_tags:
            for vlan_tag in vlan_tags:
                tag_start = tag_end = vlan_tag
                # 抽出した config をヘッダーの順番に合わせてリスト化して追加
                interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, subnet_mask, untag, tag_start, tag_end, lacp_port])
        else:
            interface_config.append([device_id, port, name, speed, duplex, negotiation, ip_address, subnet_mask, untag, tag_start, tag_end, lacp_port])

    # RoutingのConfiguration抽出
    # XML例：
        # <route>
        #     <name>10.6.1.0/24</name>
        #     <next-hop>10.5.16.250</next-hop>
        # </route>

    # routeタグの子ノードをすべて抽出
    XPath = './/routing-options/static/route'
    routes = root.findall(XPath)
    for route in routes:
        # 各変数の初期化（ループするたびに初期化する）
        dest_ip = dest_mask = gateway = metric = ''
        # '/'で宛先アドレスとマスクに分ける
        dest_ip = route.find('name').text.split('/')[0]
        dest_mask = route.find('name').text.split('/')[1]
        gateway = route.find('next-hop').text
        # 抽出した config をヘッダーの順番に合わせてリスト化して追加
        routing_config.append([device_id, dest_ip, dest_mask, gateway, metric])
    # VlanのConfiguration抽出
        # XML例：
        # <vlan>
        #     <name>vlan1</name>
        #     <description>DEFAULT_VLAN</description>
        #     <vlan-id>1</vlan-id>
        # </vlan>
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

    # 抽出した Configuration リストをCSVに変換し出力する
    export_list_to_csv(system_csv_path, system_headers, system_config)           # System
    export_list_to_csv(interface_csv_path, interface_headers, interface_config)  # Interface
    export_list_to_csv(routing_csv_path, routing_headers, routing_config)        # Routing
    export_list_to_csv(vlan_csv_path, vlan_headers, vlan_config)                 # Valn
