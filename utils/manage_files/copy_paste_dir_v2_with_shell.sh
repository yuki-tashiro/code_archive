#!/bin/bash

PROJECT_ROOT="/home/is/yuki-ta/pjt/cure"
cd "$PROJECT_ROOT"
source .venv/bin/activate

# 実行するPythonスクリプトのファイル名
PYTHON_SCRIPT="cp_dir.py"

# --- 実験番号を指定 ---
OLD_EXP_NAME="exp_001"
NEW_EXP_NAME="exp_002"

mkdir -p "${PROJECT_ROOT}/results/${NEW_EXP_NAME}"
LOG_FILE="${PROJECT_ROOT}/results/${NEW_EXP_NAME}/exp_${NEW_EXP_NAME}_setup.log"

echo "実験ディレクトリ ${NEW_EXP_NAME} を作成します．ログは ${LOG_FILE} を確認してください．"

python -u "$PYTHON_SCRIPT" \
        --base_dir "${PROJECT_ROOT}/experiments" \
        --old-exp-name "$OLD_EXP_NAME" \
        --new-exp-name "$NEW_EXP_NAME" > "$LOG_FILE" 2>&1 &


# バックグラウンドプロセスのPIDを表示
echo "スクリプトが完了しました．"