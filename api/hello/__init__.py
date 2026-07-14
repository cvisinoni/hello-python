import sys

from .version import banner
from .logger import setup_logger
from .server import Server


print(banner, file=sys.stderr)
setup_logger()


__all__ = ['Server']
