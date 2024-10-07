import pandas as pd

def print_unique_values(df, df_cols=None):
    """
    各カラムのユニーク値とそのカウント数を出力する関数

    Args:
        df (pd.DataFrame): 対象のDataFrame
        df_cols (list): 対象のカラム名のリスト
    Usage:
    df_cols = ['label', 'pipette_p_n']
    print_unique_values(df, df_cols)
    """
    for col in df_cols:
        print(f"\nカラム: {col}:")
        print(f"ユニーク値: {df[col].nunique(dropna=False)}種類")
        print(df[col].value_counts(dropna=False))

df_cols = ['label', 'pipette_p_n']
print_unique_values(df, df_cols)
