"""
# CV/LB分析

## 概要
このファイルでは、CURE-BenchのCV（交差検証）とLB（リーダーボード）を分析します。
- CV: phase1 val score
- LB: phase1 test score

"""


from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import time
import json


# グラフのスタイル設定
# plt.style.use('ggplot')
sns.set_palette("tab10")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 18


def paths_to_df(file_paths):
    """
    JSONファイルのパスを受け取り、実験名とスコアを抽出してDataFrameに変換する。

    Args:
        file_paths (list of Path): JSONファイルのパスのリスト。
    Returns:
        pd.DataFrame: 実験名とスコアを含むDataFrame。
    """
    
    exp_files = {}

    # 実験名とタイプごとにファイルを分類
    for file_path in file_paths:
        if not file_path.name.startswith("exp_"):
            continue
        exp_name = "_".join(file_path.stem.split("_")[:2])
        exp_type = file_path.stem.split("_")[2]
        # print(f"Processing {file_path.name} as {exp_name} of type {exp_type}")
        if exp_name not in exp_files:
            exp_files[exp_name] = {}
        exp_files[exp_name][exp_type] = file_path

    # val, testがある実験のみを抽出
    exp_cv_lb_files = {exp_name: types for exp_name, types in exp_files.items() if "val" in types and "test" in types}

    print(f"exp_cv_lb_files: \n{exp_cv_lb_files}")

    results = {}
    # 各実験のvalとtestのスコアを抽出
    for key, value in exp_cv_lb_files.items():
        val_file = value.get("val")
        test_file = value.get("test")
        
        # JSONファイルを読み込み
        with open(val_file, 'r') as f:
            val_data = json.load(f)
        
        with open(test_file, 'r') as f:
            test_data = json.load(f)
        
        # スコアを抽出
        val_acc_all = val_data.get("acc_all", 0)
        test_acc_all = test_data.get("acc_all", 0)
        
        results[key] = {
            "val(acc_all)": val_acc_all,
            "test(acc_all)": test_acc_all
        }

    df = pd.DataFrame.from_dict(results, orient='index').reset_index()
    df.columns = ['exp_name', 'val(acc_all)', 'test(acc_all)']
    print(df.head())

    return df


def plot_cv_lb_scores(df: pd.DataFrame, output_dir: Path, plot_exp_name: bool = True):
    """
    CVスコア(val)を横軸、LBスコア(test)を縦軸にした散布図をプロットする．

    Args:
        df (pd.DataFrame): 'exp_name', 'val(acc_all)', 'test(acc_all)' を含むDataFrame．
        output_dir (Path): グラフ画像の出力先ディレクトリ．
        plot_exp_name (bool): 実験名を注釈としてプロットするかどうか．デフォルトはTrue．
    """

    plt.style.use('seaborn-v0_8-whitegrid') # 見やすいスタイルに変更
    fig, ax = plt.subplots(figsize=(8, 8)) # 正方形のグラフ領域を作成

    # 散布図をプロット
    ax.scatter(df['val(acc_all)'], df['test(acc_all)'], s=10, alpha=0.7, zorder=5)

    # 各点に実験名を注釈として追加
    if plot_exp_name:
        for i, row in df.iterrows():
            ax.text(
                row['val(acc_all)'],
                row['test(acc_all)'],
                f" {row['exp_name']}", # 点の少し右側に表示
            fontsize=10,
            verticalalignment='center',
            zorder=10
        )

    # グラフの体裁を調整
    ax.set_title('CV vs LB')
    ax.set_xlabel('CV Score (val_acc_all)')
    ax.set_ylabel('LB Score (test_acc_all)')
    
    # 理想的な相関を示す y=x の対角線を追加
    min_val = min(ax.get_xlim()[0], ax.get_ylim()[0])
    max_val = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='y=x', zorder=1)
    
    # 軸の範囲を揃えて正方形にする
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    
    ax.legend()
    ax.set_aspect('equal', adjustable='box') # アスペクト比を1:1に固定

    # グラフをファイルに保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"cv_vs_lb_correlation_{timestamp}.png"
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show() # グラフを表示
    plt.close(fig) # メモリリークを防ぐためにFigureを閉じる
    
    print(f"グラフを '{output_file}' として保存しました．")


if __name__ == "__main__":

    LOG_DIR = Path("/home/is/yuki-ta/pjt/cure/results/cv_lb")
    OUTPUT_DIR = Path("/home/is/yuki-ta/pjt/cure/results/cv_lb_output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_paths = sorted(list(LOG_DIR.glob("*.json")))
    print(f"Found {len(file_paths)} log files.\nFiles: \n{file_paths}")

    df = paths_to_df(file_paths)
    plot_cv_lb_scores(df, OUTPUT_DIR, plot_exp_name=True)