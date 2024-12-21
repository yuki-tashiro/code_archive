import os
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

def process_image(image_path):
    """
    画像の処理を行う関数。
    """
    image = Image.open(image_path)
    width, height = image.size
    if width == 1333 and height == 743:  # 出力結果 widths_dict: {1333: 89077, 960: 12}
        image_array = np.array(image)
        del image
        return image_array
    else:
        image_array = np.zeros((743, 1333, 3), dtype=np.uint64)
        return image_array

def calculate_average_image(directory, output_path):
    """
    入力ディレクトリ内のJPG画像の平均画像を計算し、指定された出力パスに保存します。
    """

    shape = (743, 1333, 3)
    sum_array = np.zeros(shape, dtype=np.uint64)
    image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.jpg')]

    # 画像処理を並列で実行
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_image, image_path) for image_path in image_paths]
        for future in as_completed(futures):
            image_array = future.result()
            sum_array += image_array.astype(np.uint64)
            del image_array

    # 画素の平均値を計算
    avg_array = (sum_array / len(image_paths)).astype(np.uint8)

    # 平均画像を生成
    avg_image = Image.fromarray(avg_array)

    # 平均画像を保存
    avg_image.save(output_path)

# メイン処理
# directory = '/groups/gcd50654/KH/ECG/tashiro/data/re'
directory = '/groups/gcd50654/KH/ECG/data/yoboigakukyokai/PDF_data/PDF2jpg_240512'
output_path = '/groups/gcd50654/KH/ECG/tashiro/data/synthesize_avg_image.jpg'

start_time = time.time()  # 処理開始時刻

calculate_average_image(directory, output_path)

print(f'以下のパスに画像が保存されました: {output_path}')

elapsed_time = time.time() - start_time  # 経過時間（秒）
print(f"完了 - 処理時間: {elapsed_time:.3f}秒")
""" output
rt_Fで，624.74秒
その他ではkilled（メモリエラー）
"""