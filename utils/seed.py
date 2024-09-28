## 再現性確保のためのSeed固定
import random
import os
import numpy as np
import torch
""" # 使用方法
from types import SimpleNamespace
config = SimpleNamespace()
config.seed = 42
seed_everything(config.seed)
"""

def seed_everything(seed:int==42, gpu=True):
    """
    乱数生成の再現性を確保するために、Python、OS、NumPy、およびPyTorchのシードを固定します。

    Args:
        seed (int, optional): 固定したいシード値。デフォルトは42。
        gpu (bool, optional): GPUのシードも固定するかどうか。デフォルトはTrue。

    使用例:
        seed_everything(42)
        
        from types import SimpleNamespace
        config = SimpleNamespace()
        config.seed = 42
        seed_everything(config.seed)
    """

    print(f'Globas Seed {seed} set')
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)

    if gpu:

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True

