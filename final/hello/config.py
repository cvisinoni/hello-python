from pathlib import Path
from os import getenv, pathsep
from typing import Optional, Any
from configparser import ConfigParser
from datetime import datetime
import tomllib


_config_path = getenv('CONFIG_PATH')
_config_file = 'hello/hello.ini'


class ConfigNode:

    def __init__(self, data: dict):
        self._data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def _resolve(self, path: str) -> Any:
        current = self._data
        for key in path.split('.'):
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    def get(self, path: str, default: Any = None) -> Any:
        if (value := self._resolve(path)) is not None:
            if isinstance(value, dict):
                return ConfigNode(value)
            return value
        return default

    def getstr(self, path: str, default: Optional[str] = None) -> Optional[str]:
        if (result := self._resolve(path)) is not None:
            return str(result)
        return default

    def getint(self, path: str, default: Optional[int] = None) -> Optional[int]:
        if (result := self._resolve(path)) is not None:
            return int(result)
        return default

    def getfloat(self, path: str, default: Optional[float] = None) -> Optional[float]:
        if (result := self._resolve(path)) is not None:
            return float(result)
        return default

    def getbool(self, path: str, default: Optional[bool] = None) -> Optional[bool]:
        if (result := self._resolve(path)) is not None:
            if isinstance(result, bool):
                return result
            return str(result).lower() in ('true', '1', 'yes', 'on')
        return default

    def getdatetime(self, path: str, default: Optional[datetime] = None) -> Optional[datetime]:
        if (result := self._resolve(path)) is not None:
            return datetime.fromisoformat(str(result))
        return default

    def getpath(self, path: str, default: Optional[Path] = None) -> Optional[Path]:
        if (result := self._resolve(path)) is not None:
            return Path(result)
        return default


def load_config_file(file: Path) -> dict:
    data = dict()
    suffix = file.suffix.lower()

    if suffix == ".ini":
        parser = ConfigParser(interpolation=None)
        parser.read(file, encoding="utf-8")
        for section in parser.sections():
            for option in parser.options(section):
                keys = [section.lower()] + option.split(".")
                current = data
                for key in keys[:-1]:
                    current = current.setdefault(key, dict())
                current[keys[-1]] = parser.get(section, option)

    elif suffix == ".toml":
        with file.open("rb") as f:
            content = tomllib.load(f)
        data = {
            str(key).lower(): value
            for key, value in content.items()
        }

    if isinstance(data.get("root"), dict):
        for key, value in data.pop("root").items():
            if key in data:
                raise ValueError(f"Config key '{key}' is defined both in 'root' and in another section")
            data[key] = value

    return data


def load_config() -> ConfigNode:
    directories = ['.'] + (_config_path.split(pathsep) if _config_path else [])
    for directory in directories:
        file = Path(directory).expanduser() / _config_file
        if file.is_file():
            data = load_config_file(file)
            data['_loaded_config_file'] = str(file.resolve())
            return ConfigNode(data)
    return ConfigNode({})


config = load_config()
