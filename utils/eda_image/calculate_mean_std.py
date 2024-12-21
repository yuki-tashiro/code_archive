import numpy as np
from PIL import Image
import os
import albumentations as A
import cv2

def calculate_mean_std(image_paths, transform):
    mean = np.zeros(3)
    std = np.zeros(3)
    total_images = len(image_paths)

    # # Albumentationsのセンタークロップの定義
    # transform = A.Compose([
    #     A.CenterCrop(height=crop_size[0], width=crop_size[1])
    # ])

    for image_path in image_paths:
        # 画像を読み込む
        image = Image.open(image_path).convert('RGB')
        image_np = np.array(image)

        # センタークロップを適用
        cropped = transform(image=image_np)['image']

        # 正規化のための計算
        cropped = cropped / 255.0  # Normalize to [0, 1]
        mean += cropped.mean(axis=(0, 1))
        std += cropped.std(axis=(0, 1))

    mean /= total_images
    std /= total_images

    return mean, std

# 画像ファイルパスが含まれている列を取得
image_paths = df['img_path'].tolist()

# Normalize using calculated mean and std
transform = A.Compose([
    A.CenterCrop(height=1200, width=1200),
])

mean, std = calculate_mean_std(image_paths, transform)
print(f"Calculated Mean: {mean}")
print(f"Calculated Std: {std}")

# 14min
"""
Calculated Mean: [0.3091095, 0.18064324, 0.10857117]
Calculated Std: [0.22280126, 0.14290281, 0.08503526]
"""