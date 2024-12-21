"""# PDF→JPGを10万件で実行　"""


#!pip install PyMuPDF  # install

import os
import fitz
# from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor, as_completed
import time  # 時間計測用

# 変換したいPDFファイルが格納されているフォルダのパス(変更箇所)
pdf_dir = "/groups/gcd50654/KH/ECG/data/yoboigakukyokai/PDF_data"

# JPGファイルを保存するフォルダのパス(変更箇所)
# output_dir = "/groups/gcd50654/KH/ECG/tashiro/data/pdf2jpg"
output_dir = "/groups/gcd50654/KH/ECG/tashiro/data/pdf2jpg_240513"

# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def convert_to_jpg(pdf_path, output_dir):
    """PDFファイルをJPGに変換して保存する関数"""
    doc = fitz.open(pdf_path)
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    img_filename = f'{base_filename}.jpg'
    img_path = os.path.join(output_dir, img_filename)
    
    if doc.page_count > 0:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=100)  # 100 pixels/inch
        pix.save(img_path)
        print(img_path)  # 処理完了の確認

    doc.close()

def main():

    start_time = time.time()  # 処理開始時刻
    pdf_paths = []
    # ディレクトリ内およびサブディレクトリ内の全PDFを検索
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_paths.append(os.path.join(root, file))

    # with ThreadPoolExecutor(max_workers=20) as executor: # 10hかかる速度で不適切

    # ProcessPoolExecutorを使って並列処理を実行
    with ProcessPoolExecutor(max_workers=20) as executor: # ABCI上の
        futures = [executor.submit(convert_to_jpg, path, output_dir) for path in pdf_paths]
        for future in as_completed(futures):
            pass  # 全ての処理が完了するのを待つ

    end_time = time.time()  # 処理終了時刻
    elapsed_time = end_time - start_time  # 経過時間（秒）
    print(f"完了 - 処理時間: {elapsed_time:.2f}秒")

    print("完了")

if __name__ == "__main__":
    main()

