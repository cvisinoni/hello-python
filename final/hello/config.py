from pathlib import Path
from os import getenv
from typing import Optional, Any
from configparser import ConfigParser
from datetime import datetime
from functools import reduce
import tomllib
import logging


# Application info
__info__: dict[str, Any] = dict(
    name="hello-python",
    version="0.1.0"
)


# Config Path and Files
_config_path = getenv('CONFIG_PATH')
_config_files = ['hello/hello.ini', 'hello.toml']


# Logger
log = logging.getLogger(__name__)


class ConfigNode:

    def __init__(self, data: dict):
        self._data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def _resolve(self, path: str) -> Any:
        current = self._data
        for key in path.split('.'):
            if key not in current:
                return None
            current = current[key]
        return current

    def get(self, path: str) -> Any:
        value = self._resolve(path)
        if isinstance(value, dict):
            return ConfigNode(value)
        return value

    def getstr(self, path: str, default: Optional[str] = None) -> str:
        if (result := self._resolve(path)) is not None:
            return str(result)
        return default

    def getint(self, path: str, default: Optional[int] = None) -> int:
        if (result := self._resolve(path)) is not None:
            return int(result)
        return default

    def getfloat(self, path: str, default: Optional[float] = None) -> float:
        if (result := self._resolve(path)) is not None:
            return float(result)
        return default

    def getbool(self, path: str, default: Optional[bool] = None) -> bool:
        if (result := self._resolve(path)) is not None:
            if isinstance(result, bool):
                return result
            return str(result).lower() in ('true', '1', 'yes', 'on')
        return default

    def getdatetime(self, path: str, default: Optional[datetime] = None) -> datetime:
        if (result := self._resolve(path)) is not None:
            return datetime.fromisoformat(str(result))
        return default


def _merge_data(data: dict, values: dict) -> None:
    for key, value in values.items():
        key = key.lower()
        if isinstance(value, dict):
            _merge_data(data.setdefault(key, {}), value)
        else:
            data[key] = str(value)


def load_config_file(file: Path, data: dict) -> Optional[dict]:
    if not file.is_file():
        return
    suffix = file.suffix.lower()
    if suffix == '.ini':
        parser = ConfigParser()
        parser.read(file)
        for section in parser.sections():
            for option in parser.options(section):
                words = [section.lower()] + option.lower().split('.')
                if words[0] == 'root':
                    words.pop(0)
                obj = reduce(lambda d, k: d.setdefault(k, {}), words[:-1], data)
                obj[words[-1]] = parser.get(section, option)
    elif suffix == '.toml':
        with file.open('rb') as f:
            content = tomllib.load(f)
        root_key = next((key for key in content if key.lower() == 'root'), None)
        if root_key is not None and isinstance(content[root_key], dict):
            _merge_data(data, content.pop(root_key))
        _merge_data(data, content)


def load_config() -> ConfigNode:
    __info__['config_files'] = []
    data = dict()
    if _config_path:
        for directory in f'.;{_config_path}'.split(';'):
            for config_file in _config_files:
                file = Path(directory).expanduser() / config_file
                if file.is_file():
                    __info__['config_files'].append(str(file))
                    load_config_file(file, data)
    return ConfigNode(data or dict())


config = load_config()
