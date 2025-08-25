import os
from openai import OpenAI
from datasets import Dataset, DatasetDict, load_dataset
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
from pathlib import Path


system_prompt = """
# 用途
本プロンプトは、英語の設問、選択肢、および関連テキストを、日本語に高精度で翻訳することを目的としています。翻訳対象は、一般的な文章から専門的な文書まで幅広く含まれます。

# 命令
あなたは、あらゆる分野の文書を正確かつ自然に翻訳する最高レベルの翻訳家です。提供される英語のテキストを、以下の制約条件を厳守し、自然で正確な日本語に翻訳してください。

# 制約条件
- **正確性の保持**: 固有名詞、専門用語、数字、日付、固有表現は正確に翻訳してください。標準的な訳語が存在する場合はそれを用い、存在しない場合は文脈に即したカタカナ表記や補足的な説明を採用してください。
- **意味の完全な保持**: 元のテキストの意図、ニュアンス、論理構成を変更せず、忠実に伝えてください。情報の省略や追加は絶対に行わないでください。
- **自然な日本語**: 直訳調の不自然な表現は避け、日本語の読者が違和感なく読める、流暢で自然な文章にしてください。
- **フォーマットの維持**:
    - Markdownなどの書式はそのまま保持してください。
    - 段落や改行も元の構造を保持してください。

# 出力形式
翻訳された日本語のテキストのみを出力してください。余計な解説や前置きは不要です。
"""



def api_inference(question, system_prompt, client: OpenAI) -> str:

    completion = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": f"翻訳対象の英語: \n{question}\n回答: \n"},
            ]}
        ]
    )

    return completion.choices[0].message.content


def process_record(record: dict, system_prompt: str, client: OpenAI) -> dict:
    """
    1つのデータレコード（辞書）を受け取り，質問と選択肢を翻訳して返す．
    """
    processed_record = record.copy()

    # 質問 (question) を翻訳
    if 'question' in processed_record and isinstance(processed_record['question'], str):
        original_text = processed_record['question']
        translated_text = api_inference(original_text, system_prompt, client)
        processed_record["question_ja"] = translated_text

    # 選択肢 (options) を翻訳
    if 'options' in processed_record and isinstance(processed_record['options'], dict):
        translated_options = {}
        for key, value in processed_record['options'].items():
            if isinstance(value, str):
                translated_value = api_inference(value, system_prompt, client)
                translated_options[key] = translated_value
            else:
                translated_options[key] = value
        processed_record['options_ja'] = translated_options

    return processed_record


def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


if __name__ == '__main__':

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 'your_data.jsonl' を実際のファイルパスに置き換えてください
    data_type = "test_phase1"  # または "test_phase1"
    files = {
        "val_phase1": Path("/home/is/yuki-ta/pjt/cure/data/curebench_valset_pharse1.jsonl"),
        "test_phase1": Path("/home/is/yuki-ta/pjt/cure/data/curebench_testset_phase1.jsonl"),
    }
    dataset = load_jsonl(files[data_type])
    # dataset = load_jsonl(files["test_phase1"])
    # dataset = dataset[:10]
    print(f"{len(dataset)}件のデータを読み込みました．")

    print("翻訳を開始します...")
    NUM_THREADS = 100  # APIのレートリミットに応じて調整してください
    task = partial(process_record, system_prompt=system_prompt, client=client)
    processed_records = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # tqdmで進捗を表示
        results = list(tqdm(executor.map(task, dataset), total=len(dataset), desc="翻訳中"))
        processed_records.extend(results)

    print("翻訳が完了しました．")

    # --- 変更点 4: 結果をJSONLファイルに保存 ---
    output_file = f"{files[data_type].stem}_translated{files[data_type].suffix}"
    with open(output_file, 'w', encoding='utf-8') as f:
        for record in processed_records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"翻訳結果を {output_file} に保存しました．")
