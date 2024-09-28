import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, accuracy_score

def calculate_metrics(df, label_col, pred_col, threshold=0.5):
    """
    評価指標を計算する関数。

    Parameters:
    - df: pandas DataFrame
    - label_col: 真のラベルを含むカラム名
    - pred_col: 確率値の予測を含むカラム名
    - threshold: 予測を二値化するためのしきい値（デフォルトは0.5）

    Returns:
    - 指標の辞書
    """
    # ROC AUCとPR AUCを計算
    roc_auc = roc_auc_score(df[label_col], df[pred_col])
    pr_auc = average_precision_score(df[label_col], df[pred_col])

    # 混同行列を計算
    cm = confusion_matrix(df[label_col], df[pred_col].apply(lambda x: 0 if x < threshold else 1))
    tn, fp, fn, tp = cm.flatten()

    # 各評価指標を計算
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0
    recall = sensitivity  # Sensitivity = Recall
    precision = ppv  # Positive Predictive Value
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    # 結果を辞書で返す
    metrics = {
        'Accuracy': accuracy,
        'Recall': recall,
        'Precision': precision,
        'F1 Score': f1,
        'ROC AUC': roc_auc,
        'PR AUC': pr_auc,
        'Sensitivity': sensitivity,
        'Specificity': specificity,
        'PPV': ppv,
        'NPV': npv,
    }

    return metrics


import shap

def plot_feature_importance(clf, X, title='Features Inportances', save_path='importances.png'):
    """
    特徴量の重要度を可視化する関数。

    パラメータ:
    clf: 学習済みモデル (LightGBMなど、feature_importances_を持つモデル)
    X: 学習データの特徴量
    title (str): グラフのタイトル
    save_path (str): 保存する画像のパス
    """
    # 特徴量重要度を取得
    feature_imp = pd.DataFrame(sorted(zip(clf.feature_importances_, X.columns)), columns=['Value', 'Feature'])

    # 特徴量重要度の可視化
    plt.figure(figsize=(20, 10))
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value", ascending=False), palette=sns.color_palette('pastel'))

    # タイトルの設定
    plt.title(title)

    # レイアウト調整
    plt.tight_layout()

    # グラフの保存
    plt.savefig(save_path)
    print(f'グラフを {save_path} に保存しました。')

    # グラフの表示
    plt.show()


def plot_shap(model, X, y, df_cols):
    """
    SHAPによる特徴量の可視化を行う関数。

    パラメータ:
    model: 学習済みモデル
    X: 特徴量データ
    y: ターゲットデータ
    df_cols: 特徴量の列名
    """

    # SHAP値の計算
    background = shap.maskers.Independent(X, max_samples=10)
    explainer = shap.Explainer(model, background)
    shap_values = explainer(X)

    # SHAP値の可視化
    shap.plots.beeswarm(shap_values)

    # SHAP値の散布図をそれぞれのカラム別に可視化
    for col in df_cols:
        shap.plots.scatter(shap_values[:, col], color=shap_values)

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def ML_train_eval(df, df_cols, target_column, random_state=42):
    # 特徴量カラムを生成
    # feature_columns = [f"{exp_name}_pred" for exp_name in exp_names]

    # 特徴量とターゲットに分ける
    X = df[df_cols]
    y = df[target_column]

    # データを訓練データと検証データに分割
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=random_state)

    # LGBMモデルの作成
    model = lgb.LGBMClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_valid)

    # 精度を計算
    accuracy = accuracy_score(y_valid, y_pred)
    print(f"Accuracy: {accuracy:.5f}")

    # 検証データで予測（確率値を取得）
    y_pred_proba = model.predict_proba(X_valid)[:, 1]  # 正クラスの確率を取得

    # 予測をDataFrameに格納
    valid_df = pd.DataFrame({'label': y_valid, 'pred_proba': y_pred_proba})

    # 評価指標を計算
    metrics = calculate_metrics(valid_df, 'label', 'pred_proba')

    # 結果を出力
    print("------------------------------")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.5f}")

    print("------------------------------")

    # 特徴量の重要度を可視化
    plot_feature_importance(model, X)

    # shapによる可視化
    plot_shap(model, X, y, df_cols)

# 使用例
df_cols = ["age", "AC", "SBP", "DBP", "HDLC", "TG", "BS"]
target_column = "METS"
ML_train_eval(df, df_cols, target_column)

