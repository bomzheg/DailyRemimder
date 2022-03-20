import logging.config

import yaml

from app.config.db import load_db_config
from app.models.config import Config
from app.models.config.main import Paths, BotConfig

logger = logging.getLogger(__name__)


def load_config(paths: Paths) -> Config:
    with (paths.config_path / "config.yaml").open("r") as f:
        config_dct = yaml.safe_load(f)
    return Config(
        paths=paths,
        db=load_db_config(paths.config_path),
        bot=load_bot_config(config_dct["bot"])
    )


def load_bot_config(dct: dict) -> BotConfig:
    return BotConfig(
        token=dct["token"],
        log_chat=dct["log_chat"],
        superusers=dct["superusers"],
    )
