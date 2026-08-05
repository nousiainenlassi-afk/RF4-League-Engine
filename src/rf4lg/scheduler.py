"""Scheduling utilities for RF4 League Engine."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .logger import get_logger
from .models import Competition, Match, Round, Season


_logger = get_logger(__name__)


class ScheduleLoader:
    """Load season schedules from JSON files into domain models."""

    REQUIRED_FIELDS = ["round", "home_team", "away_team", "maps", "date", "start_time"]

    def __init__(self, data_root: Path | str = Path("data")) -> None:
        """Initialize the schedule loader.

        Args:
            data_root: Root path containing season data directories.
        """
        self.data_root = Path(data_root)

    def load(self, season: str) -> Season:
        """Load and parse the schedule JSON for the specified season.

        The schedule file is expected at `data/seasons/<season>/schedule.json`.
        Each entry must contain the required fields and will be converted into
        Season, Round, and Match dataclasses.

        Args:
            season: Season identifier matching the directory name under `data/seasons`.

        Returns:
            A Season instance populated with parsed rounds and matches.

        Raises:
            FileNotFoundError: If the schedule JSON file is missing.
            ValueError: If the JSON structure is invalid or required fields are missing.
        """
        schedule_path = self.data_root / "seasons" / season / "schedule.json"
        if not schedule_path.exists():
            raise FileNotFoundError(f"Schedule file not found: {schedule_path}")

        _logger.debug("Loading schedule from %s", schedule_path)
        raw_data = self._read_json(schedule_path)
        entries = self._parse_entries(raw_data, schedule_path)

        rounds: dict[int, Round] = {}
        for entry in entries:
            round_number = self._parse_round_number(entry["round"], schedule_path)
            match = self._build_match(entry, schedule_path)
            if round_number not in rounds:
                rounds[round_number] = Round(number=round_number, matches=[])
            rounds[round_number].matches.append(match)

        return Season(name=season, rounds=rounds)

    def _read_json(self, path: Path) -> Any:
        """Read JSON data from the given path."""
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in schedule file {path}: {exc}") from exc

    def _parse_entries(self, data: Any, path: Path) -> list[dict[str, Any]]:
        """Validate that the schedule JSON contains a list of entries."""
        if not isinstance(data, list):
            raise ValueError(f"Schedule file {path} must contain a JSON array of entries.")

        entries: list[dict[str, Any]] = []
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"Schedule entry {index} in {path} must be an object.")
            self._validate_fields(item, index, path)
            entries.append(item)

        return entries

    def _validate_fields(self, item: dict[str, Any], index: int, path: Path) -> None:
        """Validate required fields exist within a schedule entry."""
        missing = [field for field in self.REQUIRED_FIELDS if field not in item]
        if missing:
            raise ValueError(
                f"Schedule entry {index} in {path} is missing required fields: {', '.join(missing)}"
            )

    def _parse_round_number(self, value: Any, path: Path) -> int:
        """Parse and validate the round number value."""
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid round value in {path}: {value!r}") from exc

    def _build_match(self, entry: dict[str, Any], path: Path) -> Match:
        """Create a Match object from a validated schedule entry."""
        home_team = self._parse_string_field(entry.get("home_team"), "home_team", path)
        away_team = self._parse_string_field(entry.get("away_team"), "away_team", path)
        maps = self._parse_maps(entry.get("maps"), path)
        start_time = self._parse_start_time(entry.get("date"), entry.get("start_time"), path)

        competitions = [Competition(map_name=map_name, start_time=start_time, results=[]) for map_name in maps]
        return Match(home_team=home_team, away_team=away_team, competitions=competitions)

    def _parse_string_field(self, value: Any, field_name: str, path: Path) -> str:
        """Parse a required string field from a schedule entry."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Field '{field_name}' in {path} must be a non-empty string.")
        return value.strip()

    def _parse_maps(self, value: Any, path: Path) -> list[str]:
        """Parse the maps list from a schedule entry."""
        if not isinstance(value, list) or not value:
            raise ValueError(f"Field 'maps' in {path} must be a non-empty array of strings.")

        map_names: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"Each map name in 'maps' of {path} must be a non-empty string.")
            map_names.append(item.strip())

        return map_names

    def _parse_start_time(self, date_value: Any, start_time_value: Any, path: Path) -> datetime:
        """Parse the combined date and start time into a datetime object."""
        date_string = self._parse_string_field(date_value, "date", path)
        time_string = self._parse_string_field(start_time_value, "start_time", path)

        try:
            return datetime.fromisoformat(f"{date_string}T{time_string}")
        except ValueError as exc:
            raise ValueError(
                f"Invalid date/start_time combination in {path}: date={date_string!r}, start_time={time_string!r}"
            ) from exc
