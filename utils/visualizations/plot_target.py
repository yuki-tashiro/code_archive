import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def plot_mets_distribution(df, target):
    """
    指定されたターゲット列に基づいてMETSの分布を円グラフと棒グラフで表示する。

    パラメータ:
    df (pd.DataFrame): データフレーム。
    target (str): ターゲットとなる列名。
    """
    # ターゲットの値のカウント
    l = list(df[target].value_counts())
    circle = [l[1] / sum(l) * 100, l[0] / sum(l) * 100]
    colors = ['blue', 'red']  # 円グラフと棒グラフの色を指定

    # プロットの作成
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))

    # 円グラフの描画
    plt.subplot(1, 2, 1)
    plt.pie(circle, labels=['METS = 0', 'METS = 1'], autopct='%1.1f%%', startangle=90,
            explode=(0.1, 0), colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})
    plt.title(f'{target} Distribution (%)')

    # 棒グラフの描画
    plt.subplot(1, 2, 2)
    ax = sns.countplot(x=target, data=df, palette=colors, edgecolor='black')

    # 各棒グラフに値を表示
    for rect in ax.patches:
        ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 2, rect.get_height(),
                horizontalalignment='center', fontsize=12)

    # X軸ラベルの設定
    ax.set_xticklabels(['METS = 0', 'METS = 1'])
    plt.title(f'Cases of {target}')

    # グラフの表示
    plt.show()

# 使用例
target = 'METS'
plot_mets_distribution(df, target)
