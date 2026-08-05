"""Configuration helpers for RF4 League Engine."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class Config:
    league_name: str = "RF4 League"
    season_year: str = "2020-2021"
    data_dir: Path = Path("data")
    output_dir: Path = Path("output")


def load_config(config_path: Path | str) -> Config:
    """Load configuration from a file or path."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    # Placeholder: read and parse actual config values
    return Config()


def merge_config(base: Config, extras: Dict[str, Any]) -> Config:
    """Merge dictionary values into a Config object."""
    for key, value in extras.items():
        if hasattr(base, key):
            setattr(base, key, value)
    return base
