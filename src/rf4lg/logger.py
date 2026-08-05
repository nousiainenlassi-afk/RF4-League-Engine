"""Logging setup for RF4 League Engine."""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for RF4 League Engine.

    The logger prints to the console and uses INFO level by default. Setting
    the environment variable `RF4_DEBUG=1` enables DEBUG logging.

    Args:
        name: Logger name to configure.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        logger.setLevel(_get_log_level())
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(_get_log_level())
    logger.propagate = False
    return logger


def _get_log_level() -> int:
    """Determine logging level from environment variables."""
    if os.getenv("RF4_DEBUG") == "1":
        return logging.DEBUG
    return logging.INFO
