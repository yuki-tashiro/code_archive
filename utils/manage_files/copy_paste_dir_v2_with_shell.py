# このファイルでは，新しい実験ディレクトリを作成するための関数を定義します．
import shutil
import os
import argparse


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

    # 1. フォルダを丸ごとコピー
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', 'wandb'))
    print(f"1. フォルダがコピーされました: {destination_folder}")

    print("\n2. ファイル名の変更を開始します．\n")
    # 2. コピー先フォルダ内のファイル名を変更
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


    # 3. ファイル内容の置換
    # コピー先ディレクトリ内のすべてのファイルを走査して，中身の文字列を置換する．
    print("\n3. 情報: ファイル内容の置換を開始します．\n")
    for root, dirs, files in os.walk(destination_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # ファイルを読み込み，内容を置換　txtファイルは開くことができ，画像ファイルは開けないそう
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 文字列が含まれている場合のみ置換・書き込み処理を行う
                if old_str in content:
                    new_content = content.replace(old_str, new_str)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"  -> 内容を更新: {file_path}")
                else:
                    print(f"  -> 置換対象の文字列が見つかりません: {file_path}")
            except Exception:
                # バイナリファイルなど，テキストとして読み込めないファイルはスキップ
                pass


def main():
    parser = argparse.ArgumentParser(description="Copy and rename files in a directory.")
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory for experiments')
    parser.add_argument('--old-exp-name', type=str, required=True, help='Old experiment name (e.g., exp_004)')
    parser.add_argument('--new-exp-name', type=str, required=True, help='New experiment name (e.g., exp_005)')
    args = parser.parse_args()

    source_folder = f"{args.base_dir}/{args.old_exp_name}"
    destination_folder = f"{args.base_dir}/{args.new_exp_name}"

    copy_and_rename_files(source_folder, destination_folder, args.old_exp_name, args.new_exp_name)


if __name__ == "__main__":
    main()