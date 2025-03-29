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


def print_unique_values(df, df_cols=None):
    """
    各カラムのユニーク値とそのカウント数を出力する関数

    Args:
        df (pd.DataFrame): 対象のDataFrame
        df_cols (list): 対象のカラム名のリスト
    Usage:
    df_cols = ['label', 'categories']
    print_unique_values(df, df_cols)
    """
    for col in df_cols:
        print(f"\n column: {col}:")
        print(f"unique value: n = {df[col].nunique(dropna=False)}")
        col_dict = df[col].value_counts(dropna=False)
        print(col_dict)
        col_unique = df[col].unique()

    return col_unique


def print_unique_values(df, df_cols=None):
    """
    各カラムのユニーク値とそのカウント数を辞書で保存し、それを出力する関数。

    Args:
        df (pd.DataFrame): 対象のDataFrame
        df_cols (list): 対象のカラム名のリスト
    Usage:
    df_cols = ['label', 'categories']
    unique_values_dict = print_unique_values(df, df_cols)
    """
    unique_values_dict = {}

    for col in df_cols:
        # カラムごとの情報を保存する辞書を作成
        col_info = {}
        
        # ユニーク値の数を取得
        col_info["unique_count"] = df[col].nunique(dropna=False)
        
        # 各ユニーク値とそのカウントを取得
        col_info["value_counts"] = df[col].value_counts(dropna=False).to_dict()
        
        # ユニーク値のリストを取得
        col_info["unique_values"] = df[col].unique().tolist()

        # 辞書にカラム名で情報を保存
        unique_values_dict[col] = col_info

        # 辞書を出力
        print(f"\n columns: {col} \m")
        for col, num in col_info['value_counts'].items():
            print(f"{col}: {num}")

    return unique_values_dict


df_cols = ['t', 'n', 'm']
unique_values_dict = print_unique_values(merged_df, df_cols)