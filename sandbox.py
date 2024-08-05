import pandas as pd
import random

pd.set_option("display.max_columns", 500)
csv_path = "goi.csv"
df = pd.read_csv(csv_path)


def aggregate_and_sort(header):
    # 指定されたヘッダーの列で集計を行い、カウント数の多い順に表示
    result = df[header].value_counts().sort_values(ascending=False)

    # 結果を表示
    print(result)


def select_random_rows(header_name, header_value, num_rows=10):
    # 指定されたヘッダーと値に該当する行を抽出
    filtered_df = df[df[header_name] == header_value]

    # 該当する行が10行未満の場合は全ての行を取得
    if len(filtered_df) < num_rows:
        num_rows = len(filtered_df)

    # ランダムに10行を選択
    random_rows = random.sample(list(filtered_df.index), num_rows)

    # 選択された行の「標準的な表記」列の値を標準出力
    for idx in random_rows:
        print(filtered_df.loc[idx, "標準的な表記"])


def aggregate_by_part_of_speech(part_of_speech1):
    # 指定された「品詞1」の値に該当する行を抽出
    filtered_df = df[df["品詞1"] == part_of_speech1]

    # 「品詞2(詳細)」で集計を行い、カウント数の多い順に表示
    result = filtered_df["品詞2(詳細)"].value_counts().sort_values(ascending=False)

    return result
