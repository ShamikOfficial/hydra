# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any

from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig
from hydra.experimental.callback import Callback
from hydra.utils import execution_whitelist


class CaptureControllerHydraCallback(Callback):
    """Resolves a controller-valid ${hydra:...} value during callback construction."""

    def __init__(self, controller_cwd: str) -> None:
        self.controller_cwd = controller_cwd

    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
        print(f"controller_cwd={self.controller_cwd}")


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    # Job-specific HydraConfig must be available (id/num set during the job).
    print(f"value={cfg.value}")
    print(f"job_id={HydraConfig.get().job.id}")
    print(f"job_num={HydraConfig.get().job.num}")


if __name__ == "__main__":
    with execution_whitelist("my_app.*"):
        my_app()
