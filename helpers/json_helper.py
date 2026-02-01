import json
from pathlib import Path


def load_json(path: str):
    p = Path(path)
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        return json.load(f)
