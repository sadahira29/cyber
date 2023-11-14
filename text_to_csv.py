import csv

# configを読み込む
with open('config/juniper_config.txt', 'r') as config_txt:
	# 各行を配列linesに格納
	lines = config_txt.readlines()
	# print(lines)

# テキストファイルからCSVファイルに変換
with open('config/juniper_config.csv', 'w', newline='') as config_csv:
	writer = csv.writer(config_csv)
	print(writer)
	for line in lines:
		# 行を適切に処理してCSVファイルに書き込みます
		#print(line)
		writer.writerow(line.strip().split())