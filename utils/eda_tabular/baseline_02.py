import os
import time
import warnings
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


# 警告抑制
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

INPUT_DIR = "../data"


def write_submission(id_list, pred, output_file):
    """予測結果を出力します."""
    df = pd.DataFrame({'id': id_list, 'default': pred})
    df.to_csv(output_file, index=False)

def convert_object_columns(df):
    """特定のオブジェクト型列を適切に数値変換・カテゴリ変換する関数"""

    if 'term' in df:
        term_map = {'36 months': 36, '60 months': 60}
        df['term'] = df['term'].map(term_map).astype(int)
    if 'grade' in df:
        grade_map = {g: i+1 for i, g in enumerate(['A','B','C','D','E','F','G'])}
        df['grade'] = df['grade'].map(grade_map).astype(int)
    if 'emp_length' in df:
        emp_map = {'< 1 year':0,'1 year':1,'2 years':2,'3 years':3,'4 years':4,
                   '5 years':5,'6 years':6,'7 years':7,'8 years':8,'9 years':9,'10+ years':10}
        df['emp_length'] = df['emp_length'].map(emp_map).fillna(-1).astype(float)

    # 特徴量の追加
    # annual_inc の対数変換（外れ値緩和）
    df['annual_inc_log'] = np.log1p(df['annual_inc']).astype(float)

    # 比率・交互作用系
    # 年収に対する年間返済額比率：installment（月額返済）×12 ÷ annual_inc
    df['annual_installment_amt'] = df['installment'] * 12
    df['debt_to_income_ratio'] = df['annual_installment_amt'] / (df['annual_inc'] + 1e-6)

    # 「貸出金額あたりの利息負担感」：int_rate_float × loan_amnt
    df['interest_burden'] = df['int_rate'] * df['loan_amnt']
    # “月々の返済額 × 返済月数” で、期間中に返す総額
    df['total_payment'] = df['installment'] * df['term']

    # “総支払額 － 借入額” で、期間中に支払う利息部分
    df['total_interest'] = df['total_payment'] - df['loan_amnt']

    # 年収差額（引き算）
    df['income_minus_annual_installment'] = df['annual_inc'] - df['annual_installment_amt']
    # 貸出額／年収比率（割り算）
    df['loan_to_income_ratio'] = df['loan_amnt'] / (df['annual_inc'] + 1e-6)

    # 月収に対する返済比率（割り算）
    df['installment_to_monthly_inc'] = df['installment'] / (df['annual_inc'] / 12 + 1e-6)
    # 金利×借入額による利息負担感（掛け算）
    # int_rate がパーセント（例：11.53）なら 100 で割って実利率を適用
    df['interest_burden'] = (df['int_rate'] / 100) * df['loan_amnt']

    # テキスト系特徴量
    # title の文字数や単語数
    df['title_len_chars'] = df['title'].str.len()
    df['title_len_words'] = df['title'].str.split().str.len()

    # emp_title（職種名）の頻度エンコーディング
    freq = df['emp_title'].value_counts(normalize=True)
    df['emp_title_freq'] = df['emp_title'].map(freq)
    df['title_freq'] = df['title'].map(df['title'].value_counts(normalize=True))
    df['addr_state_freq'] = df['addr_state'].map(df['addr_state'].value_counts(normalize=True))
    df['home_ownership_freq'] = df['home_ownership'].map(df['home_ownership'].value_counts(normalize=True))
    df['purpose_freq'] = df['purpose'].map(df['purpose'].value_counts(normalize=True))

    # 和積
    df['loan_amnt_grade_multiply'] = df['loan_amnt'] * df['grade']
    df['loan_amnt_grade_divide'] = df['loan_amnt'] / (df['grade'] + 1e-6)

    if 'verification_status' in df:
        status_map = {'Not Verified':0, 'Source Verified':1, 'Verified':2}
        df['verification_status'] = df['verification_status'].map(status_map).astype(int)
    df = df.drop(columns=['home_ownership','purpose','title','addr_state', 'emp_title'], errors='ignore')
    return df

def timer(func):
    """実行時間を計測するデコレータ"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Total runtime: {elapsed:.2f} seconds")
        if elapsed > 1200:
            print("Warning: Runtime exceeded 1200 seconds limit.")
        return result
    return wrapper

@timer
def main():
    train_file = os.path.join(INPUT_DIR, 'train/train.csv')
    target_name = 'default'

    # 目的変数、説明変数を抽出します.
    train_df = pd.read_csv(train_file)
    targets = train_df[target_name]
    train_df = train_df.drop(target_name, axis=1)
    train_df = convert_object_columns(train_df)
    num_cols = [is_numeric_dtype(dtype) for dtype in train_df.dtypes]
    train_features = train_df.loc[:, num_cols]
    train_features = train_features.fillna(train_features.mean())
    mms = MinMaxScaler()
    train_features = mms.fit_transform(train_features)

    # 予測を行います.
    test_file = os.path.join(INPUT_DIR, 'test/test.csv')
    test_df = pd.read_csv(test_file)
    test_df = convert_object_columns(test_df)
    num_cols = [is_numeric_dtype(dtype) for dtype in test_df.dtypes]
    test_features = test_df.loc[:, num_cols]
    test_features = test_features.fillna(test_features.mean())
    test_features = mms.transform(test_features)
    # pred = clf.predict_proba(test_features)[:, 1]


    # y_test, ensemble_predでROCAUCの計算
    ground_truth_file = os.path.join(INPUT_DIR, 'groundtruth/ground_truth.csv')
    gt_df = pd.read_csv(ground_truth_file)
    y_gt = gt_df[target_name]
    # test_auc = roc_auc_score(y_gt, test_pred)
    # test_acc = accuracy_score(y_gt, (test_pred > 0.5).astype(int))
    # print(f"Test Accuracy: {test_acc:.4f}, Test AUC: {test_auc:.4f}")

    # モデルの学習を行います.
    X_train, X_val, y_train, y_val = train_test_split(
        train_features, targets, test_size=0.1, random_state=42
        )

    # --- モデル定義 ---
    models = [
        ("LR",  LogisticRegression(max_iter=5000, tol=1e-4, solver='saga', random_state=42)),
        ("LR2", LogisticRegression(max_iter=10000, tol=1e-2, solver='saga', random_state=42, C=0.1)),
        ("LR3", LogisticRegression(max_iter=10000, tol=1e-2, solver='sag', random_state=42, C=0.01)),
        ("LR4", LogisticRegression(max_iter=1000, tol=1e-2, solver='saga', random_state=42, C=0.001)),
        ("XGB", XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)),
        ("LGBM",LGBMClassifier(random_state=42)),
        ("LGBM2", LGBMClassifier(random_state=42, n_estimators=1000, learning_rate=0.1, verbose=0)),
        ("LGBM3", LGBMClassifier(random_state=42, n_estimators=1000, learning_rate=0.1, verbose=0, max_depth=7)),
        # ("LGBM", LGBMClassifier(random_state=42, n_estimators=10000, learning_rate=0.1, verbose=0, max_depth=7)),
        ("CatB",CatBoostClassifier(verbose=0, random_state=42)),
        ("CatB2", CatBoostClassifier(verbose=0, random_state=42, n_estimators=1000, learning_rate=0.1)),
        ("MLP",MLPClassifier( hidden_layer_sizes=(100,50), activation='relu', solver='adam', alpha=1e-4, batch_size=32, learning_rate='adaptive', learning_rate_init=1e-3, max_iter=200, random_state=42, early_stopping=True)),
    ]

    # --- 各モデルの学習と評価 ---
    preds = []
    for name, clf in models:
        clf.fit(X_train, y_train)
        prob_val = clf.predict_proba(X_val)[:, 1]
        acc = accuracy_score(y_val, (prob_val > 0.5).astype(int))
        auc = roc_auc_score(y_val, prob_val)
        print(f"{name}: Val Accuracy: {acc:.4f}, AUC: {auc:.4f}")

        # testデータに対する予測
        pred = clf.predict_proba(test_features)[:, 1]

        test_auc = roc_auc_score(y_gt, pred)
        test_acc = accuracy_score(y_gt, (pred > 0.5).astype(int))
        print(f"Test Accuracy: {test_acc:.4f}, Test AUC: {test_auc:.4f}")
        preds.append(pred)

    test_pred = np.mean(preds, axis=0)

    test_auc = roc_auc_score(y_gt, test_pred)
    test_acc = accuracy_score(y_gt, (test_pred > 0.5).astype(int))
    print(f"Final Test Accuracy: {test_acc:.4f}, Final Test AUC: {test_auc:.4f}")

    # 結果を出力します.
    output_file = os.path.join(INPUT_DIR, 'submission.csv')
    write_submission(test_df['id'], test_pred, output_file)


if __name__ == '__main__':
    main()
