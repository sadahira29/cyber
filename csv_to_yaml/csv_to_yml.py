import csv
import yaml #PyYAMLをインストールする必要あり

# CSVから辞書データに変換する関数の定義
# 引数　：CSVファイルのパス
# 返り値：CSVから変換した辞書型データ
def csv_to_dict(csv_file):
    # 空の辞書データ
    dict_data = {}
    # CSVを読み込む
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        # csvを1行ずつ読み込む
        for row in reader:
            # row(配列)の長さが１ならば
            if len(row) == 1:
                # テーブル名として取得する
                table_name = row[0]

                # テーブル名に対する辞書データの定義（空の配列）
                dict_data[table_name] = []

                # 次の行はカラムの行（のはず）
                columns_row = next(reader)

                # 以降の処理をスキップして次のループへ
                continue
            # テーブル名に対応する辞書データをリストに追加
            # zip(a,b) : リストa,bの対応する要素をタプルに変換 例：[(a1,b1),(a2,b2),...]
            # dict(c)  : タプルの1番目の要素をキー、2番目の要素を値として辞書型に変換
            dict_data[table_name].append(dict(zip(columns_row, row)))
    return dict_data

# 辞書型からYAMLに変換し、yamlファイルに書き込む関数を定義
# 引数１：辞書型データ，引数２：出力するYAMLファイルのパス
def dict_to_yaml(dict_data, yaml_file):
    # 書き込みモードでファイルを開く
    with open(yaml_file, 'w') as yml:
        # 辞書型データからYaml型データに変換
        yaml.dump(dict_data, yml, default_flow_style=False, sort_keys=False)


# 入力するCSVファイル
csv_file  = 'csv_to_yaml/example.csv'
# 出力するYamlファイル
yaml_file = 'csv_to_yaml/example.yaml'

# csv_to_dict関数の実行結果
dict_data = csv_to_dict(csv_file)

dict_to_yaml(dict_data, yaml_file)
