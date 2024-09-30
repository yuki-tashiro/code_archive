import pandas as pd

csv_path = './annotation_file.csv'
df = pd.read_csv(csv_path)
df


import pandas as pd
# CSVファイルの読み込み
df = pd.read_csv('/groups/gcd50654/KH/ECG/tashiro/data/annotations_file_100k_240512_pa_re.csv')

# img_path列の変更
df['img_path'] = df['img_path'].str.replace('jpg_12npy_240512_pa_re', 'jpg_12npy_240512_pa_re_012')

# 新しいCSVファイルに保存
df.to_csv('/groups/gcd50654/KH/ECG/tashiro/data/annotations_file_100k_240512_pa_re_012.csv', index=False)


### Excel2CSV ###----------------------------------------------------------------------------------------------------------------


import numpy as np
import pandas as pd
import random
import os

# 乱数のシードを設定
np.random.seed(1234)
random.seed(1234)

def process_excel_file(excel_path, img_dir, output_csv_path):
    """
    エクセルファイルを読み込み、画像ファイルのパスを生成し、CSVファイルとして保存する関数。

    Parameters:
    excel_path (str): エクセルファイルのパス。
    img_dir (str): 画像ファイルのディレクトリ。
    output_csv_path (str): 出力するCSVファイルのパス。

    Returns:
    None
    """
    df = pd.read_excel(excel_path, sheet_name='データ')[['JPEGファイルID', '正常=0, 異常=1']]
    df = df.rename(columns={'JPEGファイルID': 'ID', '正常=0, 異常=1': 'abn'}).replace({'0（正常）': 0, '1（異常）': 1})
    df['img_path'] = df['ID'].apply(lambda id_name: os.path.join(img_dir, id_name + '.JPG'))
    df = df[df['img_path'].apply(os.path.exists)]
    df = df.dropna(subset=['abn'])
    df['abn'] = df['abn'].astype(int)
    df.to_csv(output_csv_path, index=False)

# 関数の呼び出し
process_excel_file(
    excel_path='/groups/gcd50654/KH/ECG/tashiro/data/ID_識別データ_0822 (五十嵐先生).xlsx',
    img_dir='/groups/gcd50654/KH/ECG/tashiro/data/origin_jpg_6x2',
    output_csv_path='./data/annotations_file_6x2.csv'
)