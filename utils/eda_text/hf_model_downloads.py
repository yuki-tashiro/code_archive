#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from huggingface_hub import snapshot_download
from typing import List, Union


# simpleなバージョン
# def download_hf_model(repo_id: str):
#     """指定したリポジトリからモデルをダウンロード"""
#     snapshot_download(repo_id=repo_id)
#     print(f"✅ Model '{repo_id}' has been downloaded.")


def download_hf_model(repo_ids: Union[str, List[str]]) -> None:
    """指定したリポジトリID（またはリスト）からモデルをダウンロード。"""

    # 文字列ならリストに変換
    if isinstance(repo_ids, str):
        repo_list = [repo_ids]
    else:
        repo_list = repo_ids

    # 各リポジトリからモデルを全てダウンロード
    for repo_id in repo_list:
        snapshot_download(repo_id=repo_id)
        print(f"✅ Model '{repo_id}' has been downloaded.\n")


if __name__ == "__main__":
    # ダウンロードするモデルのリポジトリIDを指定
    REPO_ID = "unsloth/Qwen2.5-7B-Instruct-bnb-4bit"

    # モデルをダウンロード
    download_hf_model(repo_ids=REPO_ID)