"""Pythonにおけるドキュメントの記載方法を自身の中で統一するためのメモ"""

# docstringとは

# コード内で文字を記載する際の方法の一つ。
# (#)をいれることでそれ以降がコメントとなる。コメントはコード内で無視される。
# ('"""')で囲うことでdocstringとなる。


""" docstringの記載方法
主に2つのガイドによって記載方法の基本ルールが定められている。

- Pythonのコーディングスタイルガイドである PEP 8
    - https://pep8-ja.readthedocs.io/ja/latest/
- docstringのスタイルガイドである PEP 257
    - https://peps.python.org/pep-0257/
また、ガイド以外の記載スタイルにはいくつかのスタイルがある。

reStructuredTextスタイル
- Googleスタイル（個人的に使用したい）
    - https://google.github.io/styleguide/pyguide.html
- NumPyスタイル
"""

def func(arg1, arg2):
    """概要

    詳細説明

    Args:
        引数(arg1)の名前 (引数(arg1)の型): 引数(arg1)の説明
        引数(arg2)の名前 (:obj:`引数(arg2)の型`, optional): 引数(arg2)の説明

    Returns:
        戻り値の型: 戻り値の説明

    Raises:
        例外の名前: 例外の説明

    Yields:
        戻り値の型: 戻り値についての説明

    Examples:

        関数の使い方

        >>> func(5, 6)
        11

    Note:
        注意事項や注釈など

    """
    value = arg1 + arg2
    return value

# 関数においては、docstringの記載方法は以下のようになる。
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Smalltableから行を取得します。

    table_handleで表されるTableインスタンスから、指定されたキーに関連する行を取得します。
    文字列キーはUTF-8でエンコードされます。

    Args:
        table_handle: オープン状態のsmalltable.Tableインスタンス。
        keys: 各テーブル行のキーを表す文字列のシーケンス。文字列キーはUTF-8でエンコードされます。
        require_all_keys: Trueの場合、すべてのキーに値が設定されている行のみが返されます。

    Returns:
        キーを対応するテーブル行データにマッピングする辞書を返します。各行は文字列のタプルとして表されます。例えば：

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        返されるキーは常にバイト列です。keys引数のキーが辞書に存在しない場合、その行はテーブルに見つかりませんでした（そしてrequire_all_keysはFalseでなければなりません）。

    Raises:
        IOError: smalltableへのアクセス中にエラーが発生しました。
    """


# クラスにおいては、docstringの記載方法は以下のようになる。
class SampleClass:
    """クラスの概要。

    クラスの詳細情報...
    クラスの詳細情報...

    Attributes:
        likes_spam: SPAMが好きかどうかを示すブール値。
        eggs: 産んだ卵の数を示す整数。
    """

    def __init__(self, likes_spam: bool = False):
        """SPAMの好みに基づいてインスタンスを初期化します。

        Args:
            likes_spam: インスタンスがこの好みを持つかどうかを定義します。
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    @property
    def butter_sticks(self) -> int:
        """持っているバターのスティックの数。"""


# Errorメッセージについて
if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p=}')

try:
    os.rmdir(workdir)
except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                error, workdir)

# TODOのコメントについて
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.




