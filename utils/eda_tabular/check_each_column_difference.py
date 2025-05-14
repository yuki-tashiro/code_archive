import pandas as pd
import numpy as np
import itertools

def check_column_equations(df: pd.DataFrame, column_list: list[str], atol: float = 1e-5):
    """
    指定されたカラム群の中で、すべての A - B ≈ C が成立するかどうかをチェックし、成立する式のみを出力する。

    Args:
        df (pd.DataFrame): 対象のデータフレーム
        column_list (list[str]): 比較対象のカラム名リスト
        atol (float): 許容される誤差（絶対値）

    Returns:
        list[str]: 成立した式のリスト

    Usage1:
        df = pd.read_csv("your_file.csv")
        valid_equations = check_column_equations(df, ["col1", "col2", "col3"])
        print(valid_equations)
    Usage2:
        df = pd.read_csv("your_file.csv")
        all_columns = df.columns.tolist()
        check_column_equations(df, all_columns, atol=1e-6)
    """
    # 列名をクリーンアップ（空白など）
    df.columns = df.columns.str.strip()
    column_list = [col.strip() for col in column_list]

    valid_equations = []

    for col_a, col_b, col_c in itertools.permutations(column_list, 3):
        try:
            lhs = df[col_a] - df[col_b]
            rhs = df[col_c]
            is_equal = np.isclose(lhs, rhs, atol=atol, equal_nan=False)
            mismatch_count = (~is_equal).sum()

            if mismatch_count == 0:
                equation = f"{col_a} - {col_b} ≈ {col_c}"
                print(f"✅ 成立: {equation}")
                valid_equations.append(equation)
            else:
                # print(f"❌ 不一致: {col_a} - {col_b} ≈ {col_c} → {mismatch_count} 行({mismatch_count / len(df)})不一致")
                continue

        except Exception as e:
            print(f"⚠️ スキップ: {col_a}, {col_b}, {col_c} → {e}")

    # return valid_equations


# 共通カラム（注意: 'LED1 - ' の末尾に空白があると意図しないエラーが出るので修正）
df = pd.read_csv("your_file.csv")  # 例として置き換え
common_cols = ['colA', 'colB', 'colC', 'colD', 'colE', 'colF']  # 例として置き換え

check_column_equations(df, common_cols)