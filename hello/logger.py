from .config import properties
from pathlib import Path
import logging.handlers
import logging.config
import re


# Properties
level = properties.get('logging.level', logging.DEBUG)
file = properties.get('logging.file')


# Formatter
# https://docs.python.org/3/library/logging.html#logging.basicConfig
formatter = logging.Formatter('%(asctime)s - %(filename)16s:%(lineno)4d - %(levelname)8s: %(message)s')


# Namer
def namer(default_name):
    if m := re.match(r'(.+)\.([^.]+)\.([-_0-9]+)', default_name):
        default_name = f'{m.group(1)}.{m.group(3)}.{m.group(2)}'
    return default_name


def get_logger(name):
    # Logger
    log = logging.getLogger(name)
    log.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # File handler
    # https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
    if file is not None:
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        properties = dict(
            when='midnight',
            interval=1,
            backupCount=100,
            encoding='utf-8',
            delay=True,
            utc=False,
            atTime=None,
            errors=None
        )
        fh = logging.handlers.TimedRotatingFileHandler(file, **properties)
        fh.namer = namer
        fh.setLevel(level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log


log = get_logger(__package__)
