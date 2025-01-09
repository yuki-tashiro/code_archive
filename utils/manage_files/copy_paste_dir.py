# 指定のフォルダのコピペ
import shutil

old = '014'
new = '015'

# コピー元とコピー先を指定
source_folder = f"/content/drive/MyDrive/MatsuoLab/SLab/src/exp_{old}"
destination_folder = f"/content/drive/MyDrive/MatsuoLab/SLab/src/exp_{new}"

# フォルダを丸ごとコピー
shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', 'wandb'))

print(f"フォルダがコピーされました: {destination_folder}")


### -------------------------------------------------------------------------------------------------------------------------------

import shutil
import os

def copy_and_rename_files(source_folder, destination_folder, old_str, new_str):
    """
    指定したフォルダをコピーし、ファイル名に含まれる文字列を変更する。

    Args:
        source_folder (str): コピー元フォルダのパス
        destination_folder (str): コピー先フォルダのパス
        old_str (str): ファイル名で置き換えたい文字列
        new_str (str): ファイル名で置き換える文字列
    """
    # コピー先フォルダが既に存在している場合、処理を終了
    if os.path.exists(destination_folder):
        print(f"フォルダが既に存在しています: {destination_folder}")
        return

    # フォルダを丸ごとコピー
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', 'wandb'))
    print(f"フォルダがコピーされました: {destination_folder}")

    # コピー先フォルダ内のファイル名を変更
    for root, dirs, files in os.walk(destination_folder):
        for file_name in files:
            # ファイル名に old_str が含まれている場合
            if old_str in file_name:
                # 新しいファイル名を作成
                new_file_name = file_name.replace(old_str, new_str)
                
                # ファイルパスを変更
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_file_name)
                os.rename(old_path, new_path)
                print(f"ファイル名変更: {old_path} → {new_path}")


# 使用例
old = '004'
new = '005'
source_folder = f"/content/drive/MyDrive/MatsuoLab/SLab/yokoi/code/exp_{old}"
destination_folder = f"/content/drive/MyDrive/MatsuoLab/SLab/yokoi/code/exp_{new}"

copy_and_rename_files(source_folder, destination_folder, old, new)