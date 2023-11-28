import csv
import yaml #PyYAMLをインストールする必要あり

# 辞書型からYAMLに変換し、yamlファイルに書き込む関数を定義
def dict_to_yaml(dict_data, output):
    with open(output, 'w') as yml:
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)

# Step.1 辞書型データを直接定義
# 辞書型データ
dict_data = {
    'interface': [
        {'id': 1, 'name': 'IF-1'},
        {'id': 2, 'name': 'IF-2'},
        {'id': 3, 'name': 'IF-3', 'speed': 100, 'duplex': 'full'},
        {'id': 4, 'name': 'IF-4', 'speed': 100, 'duplex': 'full'}
    ],
    'vlan': [
        {'id': 1, 'name': 'DEFAULT_VLAN'},
        {'id': 2, 'name': 'VLAN_92_seg'}
    ],
}
# 辞書型からYAMLに変換
# output = 'csv_to_yaml/output.yaml'
# dict_to_yaml(dict_data, output)


# Step.2 あらかじめキーを配列で用意
def csv_to_yaml(dict_key, dict_data, input, output):
    # CSVを読み込み、辞書型に変換する
    with open(input, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for key in dict_key:
            dict_data[key] = []
            for line in reader:
                dict_data[key].append(line)
    dict_to_yaml(dict_data, output)

dict_key  = ['interface', 'vlan', 'routing']
dict_data = {}
input  = 'csv_to_yaml/csv/step2.csv'
output = 'csv_to_yaml/yaml/output3.yaml'

# csv_to_yaml(dict_key, dict_data, input, output)


# Step.3 CSVからキーを抽出する
dict_key = []
dict_data = {}
key_number = 0
input  = 'csv_to_yaml/csv/step3.csv'
output = 'csv_to_yaml/yaml/output3.yaml'

# CSVを読み込む
with open(input, 'r', newline='') as f:
    csv_dict = []
    reader = csv.reader(f)
    for line in reader:
        if len(line) == 1:
            key = line[0]
            dict_key.append(key)
            dict_data[key] = []
            header = next(reader)
            key_number += 1
            continue
        dict_data[dict_key[key_number - 1]].append(dict(zip(header, line)))

dict_to_yaml(dict_data, output)
