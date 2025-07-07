from pathlib import Path

def get_all_files(dir_path: str, ext: str = None) -> list[str]:
    """
    指定フォルダ以下のファイルを再帰的に取得します。
    Args:
        dir_path (str): 検索するディレクトリのパス
        ext (str, optional): 拡張子（例: 'jpg'、'.png'）。省略すると全ファイルを取得
    Returns:
        list[str]: マッチしたファイルパスのリスト
    Usage:
        # JPGファイルのみ取得
        jpgs = get_all_files('/path/to/dir', 'jpg')
        # 全ファイル取得
        all_files = get_all_files('/path/to/dir')
    """
    p = Path(dir_path)
    if ext:
        # ドットがあれば除去
        ext = ext.lstrip('.')
        pattern = f'*.{ext}'
        return [str(fp) for fp in p.rglob(pattern) if fp.is_file()]
    else:
        return [str(fp) for fp in p.rglob('*') if fp.is_file()]