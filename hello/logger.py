from pathlib import Path
from os import getenv
import logging.handlers
import logging.config


# Properties
level = logging.INFO


# Formatter
# https://docs.python.org/3/library/logging.html#logging.basicConfig
formatter = logging.Formatter('%(asctime)s - %(module)12s:%(lineno)3d - %(levelname)8s - %(message)s')


# Namer
def namer(default_name):
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}.{ext}"


# Console handler
def get_console_handler(level=logging.DEBUG):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch


# File handler
def get_file_handler(level=logging.DEBUG):
    filename = 'logs/console.log'
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    properties = dict(
        when='S',
        interval=1,
        backupCount=10,
        encoding='utf-8',
        delay=False,
        utc=False,
        atTime=None,
        errors=None
    )
    fh = logging.handlers.TimedRotatingFileHandler('logs/console.log', **properties)
    fh.namer = namer
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh


# Logger
log = logging.getLogger(__package__)
log.addHandler(get_console_handler())
log.addHandler(get_file_handler())
log.setLevel(getenv('LOG_LEVEL', level))
