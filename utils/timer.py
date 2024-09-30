## 処理にかかった時間と使用したメモリを計測
from contextlib import contextmanager
import time
import psutil
import os
import math

@contextmanager
def timer(name:str, slack:bool=False):

    """
    処理にかかった時間と使用したメモリを計測するコンテキストマネージャ。

    Args:
        name (str): 計測対象の名前。ログ出力に使用されます。
        slack (bool, optional): Slack通知を行うかどうか。デフォルトはFalse。

    使用例:
        with timer("処理名"):
            df_train['label'] = df_train['METS'].copy()
            df_train['label'] = df_train['label'].apply(lambda x: int(x)) # int(x[0])
    出力例:
        << make label >> Start
        << make label >> 0.6GB(-0.0GB):0.0sec
    """

    t0 = time.time()
    p = psutil.Process(os.getpid())
    m0 = p.memory_info()[0] / 2. ** 30
    print(f'<< {name} >> Start')
    yield

    m1 = p.memory_info()[0] / 2. ** 30
    delta = m1 - m0
    sign = '+' if delta >= 0 else '-'
    delta = math.fabs(delta)

    print(f"<< {name} >> {m1:.1f}GB({sign}{delta:.1f}GB):{time.time() - t0:.1f}sec")


"""# 時間の設定"""
import datetime
import pytz

def get_current_time(region: str) -> str:
    """
    指定された地域の現在の日時を取得します。
    使い方：f("{current_time}")などで名前につける
    current_time = get_current_time('Germany')  # 'Japan', 'Germany'
    output: '20240930_215104'
    """
    if region == 'Japan':
        timezone = pytz.timezone('Asia/Tokyo')
    elif region == 'Germany':
        timezone = pytz.timezone('Europe/Berlin')
    else:
        raise ValueError("Unsupported region. Please choose 'Japan' or 'Germany' or somewhere.")

    current_time = datetime.datetime.now(timezone).strftime("%Y%m%d_%H%M%S")

    return current_time

current_time = get_current_time('Japan')


