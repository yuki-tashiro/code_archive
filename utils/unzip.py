# zipファイルを解凍

import zipfile
from pathlib import Path

# 解凍するZIPファイルのパス
zip_path = Path('/content/drive/MyDrive/AI_competition/eye_ai/dataset.zip')

# 解凍先ディレクトリ
unzip_dir = Path('/content')

# 解凍先ディレクトリが存在しない場合は作成
unzip_dir.mkdir(parents=True, exist_ok=True)

# ZIPファイルの解凍
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(unzip_dir)

print(f'ZIPファイルを {unzip_dir} に解凍しました')


# --- CVPR MED ---

import gdown

# 1
# https://drive.google.com/file/d/1l8ipIwINtT2kaJIZICEpnJAw0t6gCSpJ/view?usp=drive_link
url = 'https://drive.google.com/uc?id=1l8ipIwINtT2kaJIZICEpnJAw0t6gCSpJ'
output = '/content/drive/MyDrive/CVPR_MedSAM/MedSAM/data/Dermoscopy.zip'

gdown.download(url, output, quiet=False)
print("ダウンロード完了")
!unzip /content/drive/MyDrive/CVPR_MedSAM/MedSAM/data/Dermoscopy.zip -d /content/drive/MyDrive/CVPR_MedSAM/MedSAM/data
print("実行完了")