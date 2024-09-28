import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import japanize_matplotlib # !pip install japanize_matplotlib -q


def plot_correlation_heatmap(df, df_cols, col_desc=None, title="Correlation Matrix", cmap='coolwarm'):
    """
    指定されたカラムの相関行列を計算し、ヒートマップを表示し、カラムの説明も追加する関数。

    パラメータ:
    df (pd.DataFrame): データを含むデータフレーム。
    df_cols (list): 相関行列を計算するカラムのリスト。
    col_desc (dict): 各カラムの説明を含む辞書。
    title (str): グラフのタイトル。
    cmap (str): 使用するカラーパレット（デフォルトは 'coolwarm'）。
    """
    # 相関係数の計算
    correlation_matrix = df[df_cols].corr()

    # ヒートマップの作成
    f, ax = plt.subplots(figsize=(12, 12), facecolor=None)

    # ヒートマップの描画
    sns.heatmap(correlation_matrix, annot=True, cmap=sns.color_palette(cmap, as_cmap=True),
                vmin=-1, vmax=1, center=0, square=False, linewidths=.5,
                cbar_kws={"shrink": 0.75}, mask=np.triu(correlation_matrix))

    # タイトルの設定
    ax.set_title(title, fontsize=20, loc='center')

    # カラムの説明があれば、右上に表示
    if col_desc:
        descriptions = "\n".join([f"{col}: {desc}" for col, desc in col_desc.items()])
        plt.figtext(0.4, 0.7, descriptions, wrap=True, horizontalalignment='left', fontsize=12)

    # グラフの表示
    plt.tight_layout()
    plt.show()

# 使用例
df_cols = ["age", "AC", "SBP", "DBP", "HDLC", "TG", "BS", "METS"]
col_desc = {
    "age": "検査時年齢",
    "AC": "腹囲",
    "SBP": "収縮機血圧",
    "DBP": "拡張期血圧",
    "HDLC": "HDLコレステロール",
    "TG": "トリグリセライド (中性脂肪)",
    "BS": "血糖",
    "METS": "メタボリックシンドロームの有無 (0: なし、1: あり)"
}

plot_correlation_heatmap(df, df_cols, col_desc, title="Correlation Matrix")
