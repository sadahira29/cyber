import csv

# juniperのconfigを読み込む
with open('config/juniper_config.txt', 'r') as config_txt:
  #各行を配列linesに格納
  lines = config_txt.readlines()
  print(lines)

# テキストファイルからCSVファイルに変換
# def text_to_csv():
#   config_csv = data.replace("txt", "csv")