import csv
import xml.etree.ElementTree as ET


#------------------------------------------------------
# ここから関数の定義
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
# ここからメインの処理
#------------------------------------------------------
# XMLを扱えるようにするための準備
xml_file_path = 'xml_to_csv/config.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()
# Configurationが複数存在する場合のために，
# 抽出したConfigurationを保存しておくリスト
config_lists = []


# System(管理情報)のConfiguration抽出
system_csv_path = './xml_to_csv/output/System.csv'
system_headers  = ['hostname']
system_config = []

# 指定したXPathに対応する子ノードの抽出
system_hostname = root.find(".//system/host-name")
if system_hostname is not None:
    system_config.append(system_hostname.text)
config_lists.append(system_config)
# 抽出したSystemのConfigurationをCSVに変換する
convertCSV(system_csv_path, system_headers, config_lists)
# config_listsの初期化
config_lists = []


# InterfaceのConfiguration抽出
interface_csv_path = './xml_to_csv/output/Interface.csv'
interface_headers  = ['port', 'name', 'speed', 'duplex', 'negotiation', 'ip adress', 'ip adress mask', 'untag', 'tagged start', 'tagged end', 'lacp_port']

XPath = './/interfaces/interface'
# interfaceタグの子ノードをすべて抽出
interfaces = root.findall(XPath)
for interface in interfaces:
    interface_config = []
    IF_name = interface.find('name').text.split('/')
    if IF_name[0].startswith('ge'):
        interface_port = IF_name[2]
    else:
        interface_port = ''
    interface_name = interface.find('description') # テーブル表を見た感じではdescriptionが同じものそう
    if interface_name is not None:  # is not Noneを書かないと指定したタグがないものが含まれていた時にエラーになる
        interface_config.append(interface_port)
        interface_config.append(interface_name.text)
    else:
        continue
    ether_options = interface.find('ether-options')
    if ether_options is not None:
        speed = ether_options.find('speed')
        duplex = ether_options.find('link-mode')
        interface_config.append(speed.text if speed is not None else '')
        interface_config.append(duplex.text if duplex is not None else '')
    else:
        interface_config.extend(['' for _ in range(2)])
    # 'ip adress'以降がどこに書いているかわからないため仮に''を追加する
    interface_config.extend(['' for _ in range(6)])
    config_lists.append(interface_config)

# 抽出したInterfaceのConfigurationをCSVに変換する
convertCSV(interface_csv_path, interface_headers, config_lists)
# config_listsの初期化
config_lists = []


# RoutingのConfiguration抽出
routing_csv_path = './xml_to_csv/output/Routing.csv'
routing_headers = ['dest_ip', 'dest_mask', 'gw', 'metric']

# 指定したXPathに合致したタグをすべて取得し、それぞれの値を追加する
XPath = './/routing-options/static/route'
routes = root.findall(XPath)
for route in routes:
    routing_config = []
    # '/'で宛先アドレスとマスクに分ける
    routing_config.append(route.find('name').text.split('/')[0])
    routing_config.append(route.find('name').text.split('/')[1])
    routing_config.append(route.find('next-hop').text)
    # 'metric'がどこに書いているかわからないため仮に''を追加する
    routing_config.append('')
    config_lists.append(routing_config)

# 抽出したSystemのConfigurationをCSVに変換する
convertCSV(routing_csv_path, routing_headers, config_lists)
# config_listsの初期化
config_lists = []


# VlanのConfiguration抽出
vlan_csv_path = './xml_to_csv/output/Vlan.csv'
vlan_headers = ['VlanID', 'name', 'ip adress', 'ip adress mask']

# 指定したXPathに合致したタグをすべて取得し、それぞれの値を追加する
XPath = './/vlans/vlan'
vlans = root.findall(XPath)
for vlan in vlans:
    vlan_config = []
    vlan_config.append(vlan.find('vlan-id').text)
    vlan_config.append(vlan.find('name').text)
    # 'ip adress', 'ip adress mask'がどこに書いているかわからないため仮に''を追加する
    vlan_config.extend(['' for _ in range(2)])
    config_lists.append(vlan_config)

# 抽出したSystemのConfigurationをCSVに変換する
convertCSV(vlan_csv_path, vlan_headers, config_lists)
# config_listsの初期化
config_lists = []
