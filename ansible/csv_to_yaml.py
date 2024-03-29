import csv
import yaml #PyYAMLをインストールする必要あり
import os
import sys

#------------------------------------------------------
# コマンドライン引数
# Usage: csv_to_yaml.py [device ID] [csvfile directory path] [output yamlfile]
#------------------------------------------------------
device_id = sys.argv[1]
directory_path = sys.argv[2]
yaml_file_path = sys.argv[3]

#------------------------------------------------------
# ここから関数の定義
#------------------------------------------------------

# CSVから辞書型に変換し、辞書型の変数に格納する関数
def csv_to_dict(csv_file_path, dict_data, config_name):
    # CSVファイルを読込モードで開く
    with open(csv_file_path, 'r', newline='') as f:
        # CSVを辞書型に変換する
        reader = csv.DictReader(f)
        # config名に対応する辞書型データの各行をリストに格納
        dict_data[config_name] = [row for row in reader if row["deviceID"] == device_id]

# 辞書型からYAMLに変換し、yamlファイルに出力する関数
def dict_to_yaml(dict_data, yaml_file_path):
    # 書込モードでyamlファイルを開く
    with open(yaml_file_path, 'w') as yml:
        # 辞書型データからYamlに変換し，yamlファイルに出力する
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)

#------------------------------------------------------
# ここからメインの処理
#------------------------------------------------------

# ディレクトリ内にあるCSVファイル名をリストにすべて格納する
csv_files = os.listdir(directory_path)

# 空の辞書型データ
dict_data = {}

# 各CSVファイルに対してYaml変換を行い，全体の辞書型データを作成する
for csv_file in csv_files:
    # 拡張子なしのファイル名をconfig名として取得する
    config_name, ext = os.path.splitext(os.path.basename(csv_file))
    # 拡張子がcsvの場合のみ処理
    if ext == ".csv":
        # CSVファイルの相対パスを作成する
        csv_file_path = directory_path + '/' + csv_file
        # CSVから辞書型に変換し，辞書型変数に書き込む
        csv_to_dict(csv_file_path, dict_data, config_name)

# 作成した辞書型データをYamlに変換し，yamlファイルに出力する
dict_to_yaml(dict_data, yaml_file_path)
