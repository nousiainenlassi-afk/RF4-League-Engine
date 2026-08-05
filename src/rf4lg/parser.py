"""Parsing utilities for RF4 League Engine."""

import csv
from pathlib import Path
from typing import Iterable

from .logger import setup_logger
from .models import Player


_logger = setup_logger(__name__)


class PointsTableParser:
    """Parse points table CSV files into Player objects."""

    REQUIRED_COLUMNS = ["Team", "Player", "Pts"]

    def parse(self, file_path: Path | str) -> list[Player]:
        """Read a CSV points table and return a list of Player objects.

        The parser detects UTF-8 or CP1252 encoding automatically, validates
        that required columns exist, ignores completely empty rows, and returns
        a list of Player objects.

        Args:
            file_path: The CSV file path to parse.

        Returns:
            A list of Player objects parsed from the CSV file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If required columns are missing or row values are invalid.
            UnicodeDecodeError: If the file cannot be decoded as UTF-8 or CP1252.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Points table file not found: {path}")

        encoding = self._detect_encoding(path)
        _logger.debug("Detected encoding %s for points table %s", encoding, path)

        with path.open("r", encoding=encoding, newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            self._validate_headers(reader.fieldnames, path)
            players: list[Player] = []
            for row_index, raw_row in enumerate(reader, start=2):
                if self._is_empty_row(raw_row):
                    continue
                players.append(self._parse_row(raw_row, row_index, path))

        return players

    def _detect_encoding(self, path: Path) -> str:
        """Detect whether the file is UTF-8 or CP1252 encoded."""
        raw_bytes = path.read_bytes()
        try:
            raw_bytes.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            raw_bytes.decode("cp1252")
            return "cp1252"

    def _validate_headers(self, headers: Iterable[str] | None, path: Path) -> None:
        """Validate that required CSV columns exist in the file."""
        if headers is None:
            raise ValueError(f"CSV file {path} has no header row.")

        normalized_headers = [header.strip() for header in headers if header is not None]
        missing_columns = [column for column in self.REQUIRED_COLUMNS if column not in normalized_headers]
        if missing_columns:
            raise ValueError(
                f"CSV file {path} is missing required columns: {', '.join(missing_columns)}"
            )

    def _is_empty_row(self, row: dict[str, str | None]) -> bool:
        """Return True if all values in the CSV row are empty or missing."""
        return not any((value or "").strip() for value in row.values())

    def _parse_row(self, row: dict[str, str | None], row_number: int, path: Path) -> Player:
        """Convert a CSV row into a Player object."""
        try:
            team_value = row["Team"]
            player_value = row["Player"]
            pts_value = row["Pts"]
        except KeyError as exc:
            raise ValueError(
                f"CSV file {path} is missing required column {exc.args[0]} in row {row_number}."
            ) from exc

        if team_value is None or not team_value.strip():
            raise ValueError(f"Empty Team value in row {row_number} of file {path}.")
        if player_value is None or not player_value.strip():
            raise ValueError(f"Empty Player value in row {row_number} of file {path}.")
        if pts_value is None or not pts_value.strip():
            raise ValueError(f"Empty Pts value in row {row_number} of file {path}.")

        team = team_value.strip()
        name = player_value.strip()

        try:
            total_points = int(pts_value.strip())
        except ValueError as exc:
            raise ValueError(
                f"Invalid Pts value in row {row_number} of file {path}: {pts_value!r}"
            ) from exc

        return Player(team=team, name=name, total_points=total_points, map_points=[])
