import csv
import yaml #PyYAMLをインストールする必要あり
import os
import glob

# CSVから辞書データに変換する関数の定義
# param1：変換させるCSVファイルのパス
# return：CSVから変換した辞書型データ
def csv_to_dict(csv_file):
    # CSVファイルを読み込みモードで読み込む
    with open(csv_file, 'r', newline='') as f:
        # CSVを辞書型に変換
        reader = csv.DictReader(f)
        # 辞書データとして変換された各行をリストに格納
        dict_data = [row for row in reader]
    return dict_data

# 辞書型からYAMLに変換し、yamlファイルに書き込む関数を定義
# param1：辞書型データ
# param2：出力するYAMLファイルのパス
def dict_to_yaml(dict_data, yaml_file):
    # 追記モードでファイルを開く
    with open(yaml_file, 'a') as yml:
        # 辞書型データからYaml型データに変換
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)


# CSVファイルパスをすべて取得
# csv_dir   = "csv_to_yaml_v2/csv_files"
# csv_files = os.listdir(csv_dir)
csv_files = glob.glob("csv_to_yaml_v2/csv_files/*.csv")

# 出力するYamlファイル
yaml_file = 'csv_to_yaml_v2/output.yaml'

# 各CSVファイルに対してcsv_to_dict関数とdict_to_yaml関数を実行
for csv_file in csv_files:
    dict_data = csv_to_dict(csv_file)
    dict_to_yaml(dict_data, yaml_file)

