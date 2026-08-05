"""Parsing utilities for RF4 League Engine."""

from pathlib import Path
from typing import Any

from .models import Season, Team, Match


def parse_season_file(path: Path | str) -> Season:
    """Parse season data from a file into a Season model."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Season file not found: {file_path}")

    # Placeholder implementation.
    # Replace with actual parsing logic for CSV, JSON, or custom format.
    return Season(year="2020-2021", teams=[], matches=[])


def parse_team_data(data: Any) -> Team:
    """Convert raw team data into a Team model."""
    return Team(id=int(data.get("id", 0)), name=str(data.get("name", "")))


def parse_match_data(data: Any, teams: list[Team]) -> Match:
    """Convert raw match data into a Match model."""
    home = teams[0] if teams else Team(id=0, name="Home")
    away = teams[1] if len(teams) > 1 else Team(id=1, name="Away")
    return Match(home_team=home, away_team=away, date=data.get("date"), venue=data.get("venue", ""))
