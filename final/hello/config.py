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

    def _get_value(self, path: str, default: Any = None, required: bool = False) -> Any:
        value = self._resolve(path)
        if value is None:
            if required:
                raise KeyError(f"Required configuration key '{path}' is missing")
            return default
        return value

    def get(self, path: str, default: Any = None, required: bool = False) -> Any:
        value = self._get_value(path, default, required)
        return ConfigNode(value) if isinstance(value, dict) else value

    def getstr(self, path: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
        value = self._get_value(path, default, required)
        return str(value) if value is not None else None

    def getint(self, path: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
        value = self._get_value(path, default, required)
        return int(value) if value is not None else None

    def getfloat(self, path: str, default: Optional[float] = None, required: bool = False) -> Optional[float]:
        value = self._get_value(path, default, required)
        return float(value) if value is not None else None

    def getbool(self, path: str, default: Optional[bool] = None, required: bool = False) -> Optional[bool]:
        value = self._get_value(path, default, required)
        if value is None or isinstance(value, bool):
            return value
        normalized_value = str(value).strip().lower()
        if normalized_value in ('true', '1', 'yes', 'on', 'y'):
            return True
        if normalized_value in ('false', '0', 'no', 'off', 'n'):
            return False
        raise ValueError(f"Invalid boolean configuration value for '{path}': {value!r}")

    def getdatetime(self, path: str, default: Optional[datetime] = None, required: bool = False) -> Optional[datetime]:
        value = self._get_value(path, default, required)
        return datetime.fromisoformat(str(value)) if value is not None else None

    def getpath(self, path: str, default: Optional[Path] = None, required: bool = False) -> Optional[Path]:
        value = self._get_value(path, default, required)
        return Path(value) if value is not None else None


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
