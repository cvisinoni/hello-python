from configparser import ConfigParser
from pathlib import Path


_project = __package__


def get_config_directories():
    result = []
    for parent in Path(__file__).parents:
        if (f := parent / '.config.txt').is_file():
            result.append(Path(f.read_text()) / _project)
    return [Path('.')] + result


def get_config_file():
    for directory in get_config_directories():
        for filename in (f'{_project}.ini', 'local.ini', 'application.properties'):
            file = directory / filename
            if file.is_file():
                return file
    return None


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

    file = get_config_file()

    properties = Properties()

    if file:
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
