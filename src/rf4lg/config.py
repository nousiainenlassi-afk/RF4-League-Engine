"""Configuration helpers for RF4 League Engine."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .logger import get_logger

_logger = get_logger(__name__)


@dataclass
class Config:
    """Application configuration for RF4 League Engine."""

    season: str = "2020-2021"
    max_players: int = 16
    match_times: list[str] = field(default_factory=lambda: ["18:00", "20:00"])
    encoding: str = "utf-8"


def load_config(config_path: Path | str) -> Config:
    """Load configuration values from a JSON file.

    The parser reads the JSON file at the given path, validates expected
    configuration fields, and fills in defaults for missing values.

    Args:
        config_path: Path to the JSON configuration file.

    Returns:
        A Config instance populated from the JSON file.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the JSON is invalid or configuration fields are malformed.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    _logger.debug("Loading config from %s", path)

    try:
        raw_text = path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in config file {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Unable to decode config file {path} as UTF-8: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} must contain a JSON object.")

    config = Config(
        season=_get_str(data, "season", "2020-2021", path),
        max_players=_get_int(data, "max_players", 16, path),
        match_times=_get_str_list(data, "match_times", ["18:00", "20:00"], path),
        encoding=_get_str(data, "encoding", "utf-8", path),
    )

    _logger.debug("Loaded config: %s", config)
    return config


def _get_str(data: dict[str, Any], key: str, default: str, path: Path) -> str:
    """Retrieve a string value from config data or use a default."""
    value = data.get(key, default)
    if not isinstance(value, str):
        raise ValueError(f"Config field '{key}' in {path} must be a string.")
    if not value.strip():
        raise ValueError(f"Config field '{key}' in {path} must not be empty.")
    return value.strip()


def _get_int(data: dict[str, Any], key: str, default: int, path: Path) -> int:
    """Retrieve an integer value from config data or use a default."""
    value = data.get(key, default)
    if isinstance(value, bool):
        raise ValueError(f"Config field '{key}' in {path} must be an integer, not boolean.")
    if not isinstance(value, int):
        raise ValueError(f"Config field '{key}' in {path} must be an integer.")
    if value < 0:
        raise ValueError(f"Config field '{key}' in {path} must be zero or positive.")
    return value


def _get_str_list(data: dict[str, Any], key: str, default: list[str], path: Path) -> list[str]:
    """Retrieve a list of strings from config data or use a default."""
    value = data.get(key, default)
    if not isinstance(value, list):
        raise ValueError(f"Config field '{key}' in {path} must be a list of strings.")

    normalized: list[str] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str):
            raise ValueError(
                f"Config field '{key}' in {path} must contain only strings."
                f" Invalid item at index {index}: {item!r}"
            )
        if not item.strip():
            raise ValueError(
                f"Config field '{key}' in {path} must not contain empty strings."
            )
        normalized.append(item.strip())

    return normalized
