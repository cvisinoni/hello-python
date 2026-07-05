from pathlib import Path
import logging
import logging.handlers
import logging.config

from .config import config, __info__


def setup_logger(name: str = None, *, level: str | int = logging.INFO, file: Path | str = None, propagate: bool = True):
    # Get logger
    log = logging.getLogger(name)

    # Set level
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    log.setLevel(level)

    # Set propagate
    log.propagate = propagate

    # Avoid duplicate handlers
    if log.handlers:
        log.handlers.clear()

    # Formatter
    # https://docs.python.org/3/library/logging.html#logging.basicConfig
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)20s - %(filename)20s:%(lineno)4d - %(levelname)8s: %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # File handler
    # https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
    if file:
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.handlers.TimedRotatingFileHandler(
            file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8',
            delay=True,
            utc=False,
            atTime=None,
            errors=None
        )
        fh.namer = lambda name : name.replace(".log", "") + ".log"
        fh.setLevel(level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log


_name = __info__.get('name', __package__)
_version = __info__.get('version', '0.0.0')
_level = config.getstr('logging.level', 'DEBUG')
_file = config.getstr('logging.file')
log = setup_logger(_name, level=_level, file=_file)


log.debug(f"Starting {_name} V.{_version}")
log.debug(f"logging level set to {_level}")
for file in __info__.get('config_files', []):
    log.debug(f"loaded config file: {file}")
log.debug('---')
