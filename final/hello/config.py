from configparser import ConfigParser
from pathlib import Path
from os import getenv


_config_directories = getenv('CONFIG_PATH').split(';')
_config_file = 'hello/hello.ini'


def get_properties():

    class Properties(dict):

        def get(self, __key, default=None):
            if isinstance(__key, str) and (i := __key.find('.')) > 0:
                return super().get(__key[:i], Properties()).get(__key[i+1:], default)
            return super().get(__key, default)

        def __getattribute__(self, item):
            try:
                return super().__getattribute__(item)
            except AttributeError:
                return self.get(item)

    properties = Properties()

    for directory in _config_directories:
        file = Path(directory).expanduser() / _config_file
        if file.is_file():
            config = ConfigParser()
            config.read(file)
            for section in config.sections():
                for option in config.options(section):
                    words = [section.lower()] + option.split('.')
                    if words[0] == 'root':
                        words.pop(0)
                    obj = properties
                    for word in words[:-1]:
                        obj = obj.setdefault(word, Properties())
                    obj[words[-1]] = config.get(section, option)

    return properties


properties = get_properties()
