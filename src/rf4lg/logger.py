"""Logging setup for RF4 League Engine."""

import logging


def setup_logger(name: str = "rf4lg", level: int = logging.INFO) -> logging.Logger:
    """Create and configure a logger for the package."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
