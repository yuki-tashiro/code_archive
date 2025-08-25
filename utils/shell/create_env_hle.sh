#!/bin/bash
#
# === 環境構築専用スクリプト ===
# 目的: v03のminiconda環境からuvで環境構築することに変更
# 
#
# エラーが発生した場合は、その時点でスクリプトを停止します。
set -e

echo "--- 環境構築を開始します ---"

# 事前に実行するべきコード
# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv python install 3.12

# --- 1. 初期設定 ---
ENV_NAME=".venv_llmbench"

# --- 2. モジュールのロードとCondaの初期化 ---
echo "必要なモジュールをロードします..."
module purge
module load cuda/12.6 miniconda/24.7.1-py312
module load cudnn/9.6.0
module load nccl/2.24.3

# --- 3. 環境の存在確認 ---
# もし既に環境ディレクトリが存在すれば、構築をスキップします。
# if [ -d "$ENV_NAME" ]; then
#     echo "✅ 環境ディレクトリ '$ENV_NAME' は既に存在するため、構築をスキップしました。"
#     echo "もし環境を再作成したい場合は、先に手動で 'rm -rf $ENV_NAME' を実行してください。"
#     exit 0
# fi

# --- 4. 環境の作成とパッケージインストール ---
echo "Conda環境 '$ENV_NAME' を新規作成します..."
uv venv "$ENV_NAME" --python=3.12

# 作成した環境をこのスクリプト内で有効化します。
source "$ENV_NAME/bin/activate"

# PyTorchのCUDA指定と、requirements.txtからのインストール、
# その他のパッケージを一つのコマンドで実行します。
uv pip install \
    --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cu126 \
    -r ./llm_bridge_prod/eval_hle/requirements.txt \
    torch==2.7.1+cu126 \
    torchvision==0.22.1+cu126 \
    torchaudio==2.7.1+cu126 \
    "vllm>=0.4.2" \
    datasets \
    fsspec \
    "lm-eval[vllm]" \
    wandb

echo "🎉 uv環境 '$ENV_NAME' の構築が正常に完了しました。"
echo "次に、'source $ENV_NAME/bin/activate' で環境を有効化し、計算ジョブを実行してください。"
