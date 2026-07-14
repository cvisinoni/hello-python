import logging
import logging.handlers
import re

from hello.config import config


def setup_logger() -> None:
    # Get level from config
    level_name = config.getstr('logging.level', 'DEBUG').upper()
    level = getattr(logging, level_name, None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid 'logging.level' config value: {level_name!r}")

    # Shared formatter for all handlers
    # https://docs.python.org/3/library/logging.html#logging.basicConfig
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)20s - %(filename)20s:%(lineno)4d - %(levelname)8s: %(message)s"
    )

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(max(logging.INFO, level))

    # Clear existing handlers to avoid duplicates if this function is called more than once
    root_logger.handlers.clear()

    # Console handler at DEBUG level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File namer
    namer = lambda path: re.sub(r'([^/\\]+)\.log\.([^/\\]+)$', r'\1.\2.log', path)

    # Rotating application file handler
    # https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
    if (app_file_path := config.getpath('logging.file.app')) is not None:
        app_file_path.parent.mkdir(parents=True, exist_ok=True)
        app_file_handler = logging.handlers.TimedRotatingFileHandler(
            app_file_path,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8',
            delay=True,
            utc=False,
            atTime=None,
            errors=None
        )
        app_file_handler.namer = namer
        app_file_handler.setLevel(logging.DEBUG)
        app_file_handler.setFormatter(formatter)
        root_logger.addHandler(app_file_handler)

    # Rotating errors file handler
    if (error_file_path := config.getpath('logging.file.errors')) is not None:
        error_file_path.parent.mkdir(parents=True, exist_ok=True)
        error_file_handler = logging.handlers.TimedRotatingFileHandler(
            error_file_path,
            when="midnight",
            interval=1,
            backupCount=180,
            encoding='utf-8',
            delay=True,
            utc=False,
            atTime=None,
            errors=None
        )
        error_file_handler.namer = namer
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        root_logger.addHandler(error_file_handler)

    # Application logger: full verbosity, no own handlers (inherits from root via propagate=True)
    app_logger = logging.getLogger(__package__)
    app_logger.setLevel(max(logging.DEBUG, level))

    # Log loaded config file
    if loaded_config_file := config.getstr('_loaded_config_file'):
        app_logger.debug(f"Loaded config file: {loaded_config_file}")
    else:
        app_logger.debug("No config file loaded, using default values")

    # Set third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)
