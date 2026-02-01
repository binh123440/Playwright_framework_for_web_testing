import os
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[1] / "resources" / "config.yaml"


def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return data


CONFIG = load_config()


def get(key, default=None):
    # môi trường override ưu tiên
    return os.environ.get(key, CONFIG.get(key, default))
