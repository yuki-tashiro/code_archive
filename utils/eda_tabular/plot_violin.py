import seaborn as sns
import matplotlib.pyplot as plt

def plot_violin(df, df_col, target):
    """
    指定された列のバイオリンプロットを作成し、ターゲット列で分割します。

    パラメータ:
    df (pd.DataFrame): データを含むデータフレーム。
    df_col (list): バイオリンプロットを作成する列のリスト。
    target (str): 分割に使用するターゲット列。
    """

    for col in df_col:
        plt.figure(figsize=(10, 6))
        sns.violinplot(y=col, hue=target, split=True, data=df, palette=sns.color_palette("pastel"))
        plt.title(f"Violin Plot of {col} by {target}")
        plt.xlabel(target)
        plt.ylabel(col)
        plt.legend(title=target)
        plt.show()

# 使用例
df_cols = ["age", "AC", "SBP", "DBP", "HDLC", "TG", "BS"]
target = 'METS'
plot_violin(df, df_cols, target)
