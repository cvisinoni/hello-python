import json
from pathlib import Path
from typing import Any


def load_json(file: str | Path, **kwargs) -> Any:
    with Path(file).open("r", encoding="utf-8") as fp:
        return json.load(fp, **kwargs)


def dump_json(obj: Any, file: str | Path, **kwargs) -> None:
    kwargs.setdefault("indent", 4)
    with Path(file).open("w", encoding="utf-8") as fp:
        json.dump(obj, fp, **kwargs)
