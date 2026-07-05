import logging

from .config import __info__


log = logging.getLogger(__info__.get('name', 'hello'))
