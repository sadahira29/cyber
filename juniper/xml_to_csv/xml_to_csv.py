import csv
import xml.etree.ElementTree as ET


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
# XMLを扱えるようにするための準備
xml_file_path = 'juniper/xml_to_csv/config.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()

# outputするCSVファイルのパス
output_directry    = './juniper/xml_to_csv/output/'
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

# System(管理情報)のConfiguration抽出
# 指定したXPathに対応する子ノードの抽出
system_hostname = root.find(".//system/host-name")
if system_hostname is not None:
    hostname = system_hostname.text
    # 抽出した config をリスト化して追加
    system_config.append([hostname])

# 抽出したSystemのConfigurationをCSVに変換する
convertCSV(system_csv_path, system_headers, system_config)


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
    name = port = speed = duplex = negotiation = ip_address = ip_address_mask = untag = tag_start = tag_end = lacp_port = ''

    IF_name = interface.find('name').text.split('/')
    IF_type = IF_name[0]
    port = IF_name[2] if IF_type.startswith('ge') else port
    description = interface.find('description')
    # is not Noneを書かないと指定したタグがない時にエラーになる
    name = description.text if description is not None else IF_type
    speed_tag = interface.find('ether-options/speed')
    if speed_tag is not None:
        speed  = speed_tag[0].tag.split('-')[1]
        duplex = 'full'
    # 抽出した config をリスト化して追加
    interface_config.append([name, port, speed, duplex, negotiation, ip_address, ip_address_mask, untag, tag_start, tag_end, lacp_port])

# 抽出したInterfaceのConfigurationをCSVに変換する
convertCSV(interface_csv_path, interface_headers, interface_config)


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
    # 抽出した config をリスト化して追加
    routing_config.append([dest_ip, dest_mask, gateway, metric])

# 抽出したSystemのConfigurationをCSVに変換する
convertCSV(routing_csv_path, routing_headers, routing_config)


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
    vlan_id = vlan_name = ip_address = ip_address_mask = ''
    vlan_id   = vlan.find('vlan-id').text
    vlan_name = vlan.find('name').text
    # 抽出した config をリスト化して追加
    vlan_config.append([vlan_id, vlan_name, ip_address, ip_address_mask])

# 抽出したVlanのConfigurationをCSVに変換する
convertCSV(vlan_csv_path, vlan_headers, vlan_config)
