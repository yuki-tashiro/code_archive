import csv


def csv_to_pairwise_txt(input_csv_path: str, output_txt_path: str,
                         id_col: str = 'query_id',
                         name1_col: str = 'name1',
                         name2_col: str = 'name2') -> None:
    """
    CSV を読み込んで、MetricLearningDataset_pairwise の
    .txt 形式 (query_id||name1||name2) に変換して書き出します。

    Parameters
    ----------
    input_csv_path : str
        入力の CSV ファイルパス。ヘッダ行があり、上記列名が含まれていること。
    output_txt_path : str
        出力する .txt ファイルパス。
    id_col : str
        CSV のクエリ ID を保持している列名。デフォルトは "query_id"。
    name1_col : str
        CSV の 1 番目のエンティティ名を保持している列名。デフォルトは "name1"。
    name2_col : str
        CSV の 2 番目のエンティティ名を保持している列名。デフォルトは "name2"。
    """
    with open(input_csv_path, newline='', encoding='utf-8') as csvfile, \
        open(output_txt_path, 'w', encoding='utf-8') as txtfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            qid = row[id_col].strip()
            n1  = row[name1_col].strip()
            n2  = row[name2_col].strip()
            txtfile.write(f"{qid}||{n1}||{n2}\n")

# csv_to_pairwise_txt(csv_path, txt_path,
#                     id_col='query_id',
#                     name1_col='name1',
#                     name2_col='name2')