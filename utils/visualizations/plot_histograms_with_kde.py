import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

csv_path = './annotation_file.csv'
df = pd.read_csv(csv_path)
df

def plot_histograms_with_kde(df, cols, target, bins=100):
    """
    指定された列のヒストグラムと分布ライン（KDE）を作成します。

    パラメータ:
    df (pd.DataFrame): データを含むデータフレーム。
    cols (list): ヒストグラムを作成する列のリスト。
    target (str): ターゲット列の名前。
    bins (int): ヒストグラムのビンの数。
    """
    # ターゲットのユニークな値を取得
    target_values = df[target].unique()
    colors = {0: 'blue', 1: 'red'}  # 値に応じた色を指定

    for col in cols:
        # ターゲットごとのデータをフィルタリング
        t0 = df.loc[df[target] == 0]
        t1 = df.loc[df[target] == 1]

        # 新しいプロットを作成
        plt.figure(figsize=(10, 6))
        plt.title(f"Histgram and Distribution of {col} by {target}")

        # ヒストグラムとKDEを描画
        sns.histplot(t0[col], color=colors[0], kde=True, bins=bins, label='0', alpha=0.5)
        sns.histplot(t1[col], color=colors[1], kde=True, bins=bins, label='1', alpha=0.5)

        # 上部と右側の枠線を非表示にする
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # ラベルとタイトル
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.legend(title=target)

        # グラフを表示
        plt.show()

# 使用例
df_cols = ["age", "AC", "SBP", "DBP", "HDLC", "TG", "BS"]
target = 'METS'
plot_histograms_with_kde(df, df_cols, target)
