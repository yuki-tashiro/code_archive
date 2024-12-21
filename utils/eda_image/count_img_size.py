# ----------------------------------------
# 画像のサイズを確認する
# ----------------------------------------

from PIL import Image
import pandas as pd
import os

def directory_image_paths(directory, extensions = '.png'):
    """
    指定されたディレクトリ内の指定された拡張子の画像ファイルのパスのリストを返します。
    """
    return [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(extensions)]

def calculate_collect_image_sizes(image_paths):
    data = []
    
    for path in image_paths:
        try:
            with Image.open(path) as img:
                width, height = img.size
                channels = len(img.getbands())
                data.append({"path": path, "width": width, "height": height, "channels": channels})
        except Exception as e:
            print(f"Failed to process {path}: {e}")
    
    # DataFrameとしてまとめる
    df = pd.DataFrame(data, columns=["path", "width", "height", "channels"])
    
    # 幅と高さの組み合わせをカウント
    size_counts = df.groupby(["width", "height", "channels"]).size().reset_index(name="count")
    
    return df, size_counts

# 使用例
dir_path = "/mnt/tashiro/datacollect/annotation-image"
image_paths = directory_image_paths(dir_path, extensions = '.png')
df, size_counts = calculate_collect_image_sizes(image_paths)

# 結果を表示
print("\nImage Size Counts:")
print(size_counts)  # 幅と高さの組み合わせのカウント