import zipfile
import sys
import os

def unzip_file(zip_path, extract_to):
    """
    ZIPファイルを解凍する関数

    Args:
        zip_path (str): 解凍するZIPファイルのパス
        extract_to (str): 解凍先のディレクトリ
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted all files to {extract_to}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python unzip_file.py <zip_path> <extract_to>")
        sys.exit(1)

    zip_path = sys.argv[1]
    extract_to = sys.argv[2]

    if not os.path.exists(zip_path):
        print(f"Error: The file {zip_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    unzip_file(zip_path, extract_to)