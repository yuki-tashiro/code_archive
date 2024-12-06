"""tqdmの実用方法をまとめたモジュール"""

from tqdm import tqdm
import time


for index, row in tqdm(df.iterrows(), total=len(df), desc="checking data"):
    time.sleep(0.1)  # 何か処理をする
    print