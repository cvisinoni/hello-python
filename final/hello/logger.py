from .config import properties
import logging.handlers
import logging.config


# Properties
level = properties.get('logging.level', logging.DEBUG)


# Formatter
# https://docs.python.org/3/library/logging.html#logging.basicConfig
formatter = logging.Formatter('%(asctime)s - %(filename)16s:%(lineno)4d - %(levelname)8s: %(message)s')


def get_logger(name):
    # Logger
    log = logging.getLogger(name)
    log.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


log = get_logger(__package__)
