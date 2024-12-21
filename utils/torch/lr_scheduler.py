# ---------------------------------------------------------------------
# Warmup付きschedulerの実装。コピペして使用
# ref: https://zenn.dev/inaturam/articles/e0fa6eed17afbe
# ---------------------------------------------------------------------
import math
import torch


class CosineAnnealingLR(torch.optim.lr_scheduler._LRScheduler):
    def __init__(
        self,
        optimizer: torch.optim.Optimizer,
        warmup_epochs: int,
        max_epochs: int,
        warmup_start_lr: float = 0.00001,
        eta_min: float = 0.00001,
        last_epoch: int = -1,
    ):
        """
        Args:
            optimizer (torch.optim.Optimizer): 最適化手法インスタンス
            warmup_epochs (int): 線形warmupを行うepoch数
            max_epochs (int): cosine曲線の終了に用いる学習のepoch数
            warmup_start_lr (float): 線形warmupの初期学習率
            eta_min (float): cosine曲線の最小学習率
            last_epoch (int): 学習開始時のepoch数, cosine曲線の位相オフセット
        Note:
            学習率をmax_epochsに至るまでコサイン曲線に沿ってスケジュールする
            epoch 0からwarmup_epochsまでの学習曲線は線形warmupがかかる
            https://pytorch-lightning-bolts.readthedocs.io/en/stable/schedulers/warmup_cosine_annealing.html
        Usage:
            # warmup付きCosineLRSchedulerの実装: https://timm.fast.ai/SGDR#CosineLRScheduler
            scheduler = CosineAnnealingLR(
                optimizer,
                max_epochs = config.epochs * len(train_loader),
                warmup_epochs = config.epochs / 10 * len(train_loader), # 基本的に1/10epochでありがち
                warmup_start_lr = 1e-6,
                eta_min=1e-8,
                last_epoch = -1,
            )
        """
        self.warmup_epochs = warmup_epochs
        self.max_epochs = max_epochs
        self.warmup_start_lr = warmup_start_lr
        self.eta_min = eta_min
        super().__init__(optimizer, last_epoch)
        return None

    def get_lr(self):
        if self.last_epoch == 0:
            return [self.warmup_start_lr] * len(self.base_lrs)
        if self.last_epoch < self.warmup_epochs:
            return [
                group["lr"] + (base_lr - self.warmup_start_lr) / (self.warmup_epochs - 1)
                for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)
            ]
        if self.last_epoch == self.warmup_epochs:
            return self.base_lrs
        if (self.last_epoch - 1 - self.max_epochs) % (2 * (self.max_epochs - self.warmup_epochs)) == 0:
            return [
                group["lr"] + (base_lr - self.eta_min) * (1 - math.cos(math.pi / (self.max_epochs - self.warmup_epochs))) / 2
                for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)
            ]

        return [
            (1 + math.cos(math.pi * (self.last_epoch - self.warmup_epochs) / (self.max_epochs - self.warmup_epochs)))
            / (1 + math.cos(math.pi * (self.last_epoch - self.warmup_epochs - 1) / (self.max_epochs - self.warmup_epochs)))
            * (group["lr"] - self.eta_min)
            + self.eta_min
            for group in self.optimizer.param_groups
        ]