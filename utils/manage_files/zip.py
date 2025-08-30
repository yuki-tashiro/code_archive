import os

def zip_directory(zip_path, target_dir):
    """
    指定されたディレクトリをZIPファイルに圧縮する関数。

    Args:
        zip_path (str): 作成するZIPファイルのパス
        target_dir (str): 圧縮対象のディレクトリのパス
    """
    if os.path.exists(target_dir):
        # コマンドでZIPファイルを作成
        os.system(f'zip -r "{zip_path}" "{target_dir}"')
        print(f"Successfully zipped: {target_dir} to {zip_path}")
    else:
        print(f"Error: Target directory {target_dir} does not exist.")

# 使用例
zip_path = "./dataset.zip"
target_dir = "./第5回日本眼科AI学会総会 眼科AIコンテスト"

# 関数を呼び出してZIPファイルを作成
zip_directory(zip_path, target_dir)


#######################################################################################################################
# zipに変換するコード(遅い)
import shutil

shutil.make_archive(base_name = '/content/drive/MyDrive/BFE_Lab_2025_0214', format='zip', root_dir='/content/drive/MyDrive/BFE_Lab')

#######################################################################################################################
# urlからzipをダウンロードして解凍するコード(進捗と速度を表示)

import os
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

def download_and_extract_with_progress(url, save_path, extract=False):
    """
    指定されたURLからファイルをダウンロードし、進捗と速度をリアルタイムで表示します．
    必要に応じて解凍も行います．

    パラメータ:
    url (str): ダウンロードするファイルのURL．
    save_path (str): ファイルを保存するパス．
    extract (bool): Trueの場合、ダウンロードしたファイルを解凍します．

    使用例:
    >>> url = "https://example.com/file.zip"
    >>> save_path = "downloads/file.zip"
    >>> download_and_extract_with_progress(url, save_path, extract=True)
    """
    # 保存先のディレクトリを作成
    save_path = Path(save_path)
    directory = save_path.parent
    if not directory.exists():
        directory.mkdir(parents=True)
        print(f"ディレクトリを作成しました: {directory}")

    response = requests.get(url, stream=True)
    response.raise_for_status()  # ステータスコードが200番台でない場合は例外を発生させる

    # ヘッダーから合計ファイルサイズを取得
    total_size = int(response.headers.get('content-length', 0))

    # チャンクサイズを定義
    # chunk_size = 8192  # 8KB
    chunk_size = 1024 * 1024  # 1MB

    print(f"'{save_path.name}' をダウンロード中...")
    # tqdmを使用してプログレスバーとダウンロード情報を表示
    with open(save_path, "wb") as file, tqdm(
        desc=save_path.name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,  # KB, MB の単位に自動変換
        ncols=100, # プログレスバーの幅
    ) as bar:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # keep-aliveな新しいチャンクを除外
                size = file.write(chunk)
                bar.update(size)  # プログレスバーを更新

    print("ダウンロードが完了しました．")

    # 解凍する場合
    if extract and save_path.suffix == '.zip':
        print("ファイルを解凍中...")
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            # Zipファイル内のファイルリストでプログレスバーを作成
            file_list = zip_ref.infolist()
            extract_path = str(save_path.parent)
            with tqdm(total=len(file_list), desc="解凍中", ncols=100) as pbar:
                for member in file_list:
                    zip_ref.extract(member, extract_path)
                    pbar.update(1)
        print("解凍が完了しました．")


# --- 使用例 ---
url = "https://uni-siegen.sciebo.de/s/HGdUkoNlW1Ub0Gx/download"
save_path = "/content/drive/MyDrive/dataset/data/WESAD/WESAD.zip"
download_and_extract_with_progress(url, save_path, extract=True)


#######################################################################################################################

import os
import requests
import zipfile


def download_and_extract(url, save_path, extract=False):
    """
    指定されたURLからファイルをダウンロードし、必要に応じて解凍します。

    パラメータ:
    url (str): ダウンロードするファイルのURL。
    save_path (str): ファイルを保存するパス。
    extract (bool): Trueの場合、ダウンロードしたファイルを解凍します。

    使用例:
    >>> url = "https://example.com/file.zip"
    >>> save_path = "downloads/file.zip"
    >>> download_and_extract(url, save_path, extract=True)
    """
    # 保存先のディレクトリを作成
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # ファイルをダウンロード
    response = requests.get(url)

    with open(save_path, "wb") as file:
        file.write(response.content)

    print("ダウンロードが完了しました。")

    # 解凍する場合
    if extract:
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            extract_path = os.path.dirname(save_path)
            zip_ref.extractall(extract_path)
        print("解凍が完了しました。")

# 使用例
url = "https://uni-siegen.sciebo.de/s/HGdUkoNlW1Ub0Gx/download"
save_path = "/content/drive/MyDrive/MatsuoLab/SLab/data/WESAD/WESAD.zip"
download_and_extract(url, save_path, extract=True)

#######################################################################################################################

import zipfile

def calculate_zip_size(zip_path):
    total_size = 0

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            total_size += file_info.file_size

    size_mb = total_size / (1000 * 1000)
    size_gb = total_size / (1000 * 1000 * 1000)

    return size_mb, size_gb

# 使用例
# zip_path = "/content/drive/MyDrive/MatsuoLab/SLab/data/cuff_less_blood_pressure_estimation/cuff_less_blood_pressure_estimation.zip"
zip_path = "/content/drive/MyDrive/MatsuoLab/SLab/data/WESAD/WESAD.zip"
size_mb, size_gb = calculate_zip_size(zip_path)
print(f"ZIPファイルの総データ量: {size_mb:.2f} MB, {size_gb:.2f} GB")


# モデル(.pth)ダウンロード
import gdown

# ref: https://drive.usercontent.google.com/download?id=18Zed-TUTsmr2zc5CHUWd5Tu13nb6vq6z&authuser=0
url = 'https://drive.google.com/uc?id=18Zed-TUTsmr2zc5CHUWd5Tu13nb6vq6z'
output = '/content/MedSAM/work_dir/LiteMedSAM/lite_medsam.pth'  # 保存先のパスとファイル名
gdown.download(url, output, quiet=False)


# folderをダウンロード
# https://drive.google.com/file/d/1l8ipIwINtT2kaJIZICEpnJAw0t6gCSpJ/view?usp=drive_link
url = 'https://drive.google.com/uc?id=1l8ipIwINtT2kaJIZICEpnJAw0t6gCSpJ'
output = '/content/drive/MyDrive/CVPR_MedSAM/MedSAM/data/Dermoscopy.zip'

gdown.download(url, output, quiet=False)
print("ダウンロード完了")
!unzip /content/drive/MyDrive/CVPR_MedSAM/MedSAM/data/Dermoscopy.zip -d /content/drive/MyDrive/CVPR_MedSAM/MedSAM/data





