import pandas as pd
from sklearn.metrics import confusion_matrix, roc_auc_score, average_precision_score, precision_recall_curve, auc
import matplotlib.pyplot as plt

def evaluate_metrics(df, label_col, pred_col):
    """包括的な評価指標の計算とプロット
    acc, f1, prauc, f1系のプロットなどができる

    Args:
        df (pd.DataFrame): _description_
        label_col (str): _description_
        pred_col (str): _description_
    """

    cm = confusion_matrix(df[label_col], df[pred_col].apply(lambda x: 0 if x < 0.5 else 1))
    tn, fp, fn, tp = cm.flatten()

    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    ppv = tp / (tp + fp)
    npv = tn / (tn + fn)

    prob_th = df[df['label']==1]['pred'].min()


    # Precision-Recallカーブの計算
    precision, recall, thresholds = precision_recall_curve(df[label_col], df[pred_col])
    f1_scores = 2 * (precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1])

    # 閾値 vs Recall & Precision のプロット
    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, precision[:-1], label="Precision", marker='o', markersize=2)
    plt.plot(thresholds, recall[:-1], label="Recall", marker='o', markersize=2)
    plt.plot(thresholds, f1_scores, label="F1-score", marker='o', markersize=2)

    plt.xlabel("Threshold")
    plt.ylabel("Score")
    plt.title("Threshold vs Precision & Recall")
    plt.legend()
    plt.grid()
    plt.show()

    prauc = average_precision_score(df[label_col], df[pred_col])
    rocauc = roc_auc_score(df[label_col], df[pred_col])


    print(f'PR-AUC: {prauc:.5f}')
    print(f'ROC-AUC: {rocauc:.5f}')
    print(f'感度: {sensitivity:.4f} | 特異度: {specificity:.4f}')
    print(f'感度, 特異度: \n{sensitivity:.4f}\n{specificity:.4f}')
    print(f'陽性的中率: {ppv:.4f} | 陰性的中率: {npv:.4f}')

    metrics = {
        "probability_threshold": prob_th,
        "PR-AUC": f'{prauc:.5f}',
        "ROC-AUC": f'{rocauc:.5f}',
        "感度": f'{sensitivity:.4f}',
        "特異度": f'{specificity:.4f}',
        "陽性的中率": f'{ppv:.4f}',
        "陰性的中率": f'{npv:.4f}',
    }
    return metrics


if __name__ == '__main__':

    exp_name = 'exp_xxx'
    # val
    type = 'fold1'  # 'test', 'fold1': validation

    OUTPUT_DIR = f'/path/{exp_name}'
    path = f'{OUTPUT_DIR}/{exp_name}_{type}_pred.csv'
    df_test = pd.read_csv(path)

    metrics = evaluate_metrics(df_test, 'label', 'pred')
    print(metrics)
