import csv
import yaml #PyYAMLをインストールする必要あり
import glob

# CSVから辞書データに変換する関数の定義
# 引数１：CSVファイルのパス、引数２：空の辞書データ
# 返り値：CSVから変換した辞書型データ
def csv_to_dict(csv_file, dict_data):
    # CSVファイルを読み込みモードで読み込む
    with open(csv_file, 'r', newline='') as f:
        # CSVを辞書型に変換
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
            dict_data.update(row)
        print(dict_data)
    return dict_data

# 辞書型からYAMLに変換し、yamlファイルに書き込む関数を定義
# 引数１：辞書型データ，引数２：出力するYAMLファイルのパス
def dict_to_yaml(dict_data, yaml_file):
    # 追記モードでファイルを開く
    with open(yaml_file, 'a') as yml:
        # 辞書型データからYaml型データに変換
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)

# 空の辞書データ
dict_data = {}
# CSVファイルパスをすべて取得
csv_files = glob.glob("csv_to_yaml_v2/csv_files/*.csv")
# 出力するYamlファイル
yaml_file = 'csv_to_yaml_v2/output.yaml'

# 各CSVファイルに対してcsv_to_dict関数とdict_to_yaml関数を実行
for csv_file in csv_files:
    dict_data = csv_to_dict(csv_file, dict_data)
    dict_to_yaml(dict_data, yaml_file)

