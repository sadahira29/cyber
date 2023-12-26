import csv
import yaml #PyYAMLをインストールする必要あり
import os
import glob

#------------------------------------------------------
# ここから関数の定義
#------------------------------------------------------

def csv_to_dict(csv_file_path, dict_data, table_name):
    """
    CSVから辞書型に変換し、入力された辞書型の変数に書込む関数

    Args:
        csv_file_path (String): 変換させるCSVファイルの相対パス
        dict_data (dictionary): 格納する辞書型変数
        table_name (String)   : 現在のCSVファイルのテーブル名
    """
    # CSVファイルを読込モードで開く
    with open(csv_file_path, 'r', newline='') as f:
        # CSVを辞書型に変換する
        reader = csv.DictReader(f)
        # テーブル名に対応する辞書型データの各行をリストに格納
        dict_data[table_name] = [row for row in reader]

def dict_to_yaml(dict_data, yaml_file):
    """
    辞書型からYAMLに変換し、yamlファイルに出力する関数

    Args:
        dict_data (dictionary): 変換させる辞書型変数
        yaml_file (String)    : 出力するYAMLファイルの相対パス
    """
    # 書込モードでyamlファイルを開く
    with open(yaml_file, 'w') as yml:
        # 辞書型データからYamlに変換し，yamlファイルに出力する
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)

#------------------------------------------------------
# ここからメインの処理
#------------------------------------------------------

# CSVファイルがあるディレクトリのパス
csv_dir   = "./csv_to_yaml_v2/csv_files/"
# ディレクトリ内にあるCSVファイル名をすべて取得する
csv_files = os.listdir(csv_dir)
# 出力するYamlファイルの相対パス
yaml_file = './csv_to_yaml_v2/output.yaml'
# 空の辞書型データ
dict_data = {}

# 各CSVファイルに対してYaml変換を行い，全体の辞書型データを作成する
for csv_file in csv_files:
    # 拡張子なしのファイル名をテーブル名として取得する
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    # CSVファイルの相対パスを作成する
    csv_file_path = csv_dir + csv_file
    # CSVから辞書型に変換し，辞書型変数に書き込む
    csv_to_dict(csv_file_path, dict_data, table_name)

# 作成した辞書型データをYamlに変換し，yamlファイルに出力する
dict_to_yaml(dict_data, yaml_file)
