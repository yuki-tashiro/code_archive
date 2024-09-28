import numpy as np
import pandas as pd
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import cv2  # OpenCV を使用
import albumentations as A
from matplotlib import cm  # カラーマップ用

"""
!pip install umap-learn -q
!pip install pacmap -q # https://github.com/YingfanWang/PaCMAP
"""

import umap
import pacmap

# データの読み込み
csv_path = './annotation_file.csv'
df = pd.read_csv(csv_path)
df_reducer = df.copy()

df_col = ["age", "AC", "SBP", "DBP", "HDLC", "TG", "BS", "METS"]

# albumentationsでの前処理用のトランスフォーマーを作成
transform = A.Compose([
    A.CenterCrop(1200, 1200),  # 中央クロップ
    A.Resize(256, 256),        # リサイズ
    # A.Normalize(mean=(0.5,), std=(0.5,), max_pixel_value=255.0)  # 正規化
])

def remove_outliers(y):
    """
    四分位範囲(IQR)を使って外れ値を削除する関数
    """
    q1 = np.percentile(y, 25)
    q3 = np.percentile(y, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    # 外れ値を削除したデータと、そのインデックスを返す
    mask = (y >= lower_bound) & (y <= upper_bound)
    return y[mask], mask

def load_and_preprocess_image(img_path):
    """
    画像を OpenCV で読み込み、Albumentations を使用して前処理を行う。
    グレースケール化、クロップ、リサイズ、正規化後に1次元配列にフラット化する。
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(f"Image at {img_path} could not be loaded.")

    # Albumentations を使って画像を前処理
    augmented = transform(image=img)
    processed_img = augmented['image']

    # フラット化して返す
    return processed_img.flatten()


def run_dimensionality_reduction(df, method="tsne", n_dimention=2, remove_outliers_flag=False):
    """
    次元削減を実行する関数。指定した手法に基づいて、画像データを次元削減し、結果をプロットおよびCSVファイルに保存する。

    Parameters:
    df (pandas.DataFrame): 画像ファイルパスやラベルを含むデータフレーム。
    method (str): 次元削減手法の名前。対応手法: 'pca', 'tsne', 'umap', 'pacmap'。
    n_dimention (int): 次元削減後の次元数（2または3）。
    remove_outliers_flag (bool): 外れ値処理を行うかどうかのフラグ。

    Returns:
    None
    """
    # 画像データを格納するリスト
    X_train_data = []

    # 画像データの読み込みと前処理
    for img_path in df['img_path']:
        img_data = load_and_preprocess_image(img_path)
        X_train_data.append(img_data)

    # numpy配列に変換
    X_train_data = np.array(X_train_data)

    # 次元削減の手法を選択
    if method == "pca":
        reducer = PCA(n_components=n_dimention)
    elif method == "tsne":
        reducer = TSNE(n_components=n_dimention, random_state=42)
    elif method == "umap":
        reducer = umap.UMAP(n_components=n_dimention, random_state=42)
    elif method == "pacmap":
        reducer = pacmap.PaCMAP(n_components=n_dimention, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0)
    else:
        raise ValueError(f"Unknown method: {method}. Supported methods are: 'pca', 'tsne', 'umap', 'pacmap'")

    # 次元削減の実行
    embedding = reducer.fit_transform(X_train_data)

    # 出力をcsvで保存
    columns = [f'Component {i+1}' for i in range(n_dimention)]
    df_reducer = pd.DataFrame(embedding, columns=columns)

    # 指定された各カラムに対して結果をプロット
    for col in df_col:
        Y_label = df[col].values  # 各カラムの連続値を取得
        df_reducer[col] = Y_label  # 各カラムの Y_label を追加

        if remove_outliers_flag:
            # 外れ値を削除する場合
            Y_label_cleaned, mask = remove_outliers(Y_label)
            embedding_cleaned = embedding[mask]  # 外れ値を削除したデータに対応する埋め込みデータ
        else:
            # 外れ値処理をしない場合
            Y_label_cleaned = Y_label  # ラベルはそのまま
            embedding_cleaned = embedding  # 埋め込みデータもそのまま

        # プロットを作成
        plt.figure(figsize=(10, 8))

        # カラーマップを使用して色をつける
        norm = plt.Normalize(vmin=Y_label_cleaned.min(), vmax=Y_label_cleaned.max())
        cmap = cm.plasma  # カラーマップの選択 plasma, viridis

        if n_dimention == 2:
            # 2次元散布図
            sc = plt.scatter(embedding_cleaned[:, 0], embedding_cleaned[:, 1], c=Y_label_cleaned, cmap=cmap, s=10, norm=norm)
            plt.xlabel('Component 1')
            plt.ylabel('Component 2')
        elif n_dimention == 3:
            # 3次元散布図
            from mpl_toolkits.mplot3d import Axes3D
            ax = plt.figure().add_subplot(111, projection='3d')
            sc = ax.scatter(embedding_cleaned[:, 0], embedding_cleaned[:, 1], embedding_cleaned[:, 2], c=Y_label_cleaned, cmap=cmap, s=10, norm=norm)
            ax.set_xlabel('Component 1')
            ax.set_ylabel('Component 2')
            ax.set_zlabel('Component 3')

        # カラーバーを表示
        plt.colorbar(sc, label=col)  # カラーバーのラベルにカラム名を使用
        plt.title(f'{method.upper()} Visualization of {col} ({"Outliers Removed" if remove_outliers_flag else "No Outlier Removal"})')

        # プロットを保存
        plt.savefig(f'./output_{method}_{col}{"_outliers_removed" if remove_outliers_flag else ""}.png')
        plt.show()

    # 次元削減結果をCSVに保存
    df_reducer.to_csv(f'./output_{method}_{n_dimention}D.csv', index=False)

# 関数の呼び出し例
run_dimensionality_reduction(df, method="tsne", n_dimention=2, remove_outliers_flag=True)

