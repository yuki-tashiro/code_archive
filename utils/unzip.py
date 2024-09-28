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