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
