import json

def json_load(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

table_json_path = "/content/drive/MyDrive/MatsuoLab/LLaVA-Med-JP/data/all_tables.json"
table_data = json_load(table_json_path)

for label, tables in table_data.items():
    print(f"{label}: {tables}")