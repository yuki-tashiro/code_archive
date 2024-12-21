# ファイルの移動（33s）

from pathlib import Path

def move_files_recursively(source_dir: Path, target_dir: Path):
    # 移動先ディレクトリが存在しない場合は作成
    target_dir.mkdir(parents=True, exist_ok=True)

    # ソースディレクトリ内のすべてのファイルとサブディレクトリを処理
    for item in source_dir.iterdir():
        target_item = target_dir / item.name

        if item.is_dir():
            # サブディレクトリの場合、再帰的に処理
            move_files_recursively(item, target_item)
        elif item.is_file():
            # ファイルの場合、移動
            item.rename(target_item)

# 移動元ディレクトリ
source_dir = Path('/content/drive/MyDrive/AI_competition/eye_ai/content/drive/MyDrive/AI_competition/eye_ai/第5回日本眼科AI学会総会 眼科AIコンテスト')
# 移動先ディレクトリ
target_dir = Path('/content/drive/MyDrive/AI_competition/eye_ai/dataset')

# ファイルを再帰的に移動
move_files_recursively(source_dir, target_dir)
