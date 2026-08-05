"""Parsing utilities for RF4 League Engine."""

import csv
import logging
from pathlib import Path
from typing import Iterable, Iterator, List

from .logger import setup_logger
from .models import Player


_logger = setup_logger(__name__)


class PointsTableParser:
    """Parse points table CSV files into league player models."""

    REQUIRED_COLUMNS = ["team", "name", "map_points"]

    def parse(self, file_path: Path | str) -> list[Player]:
        """Read a CSV points table and return a list of Player objects.

        The parser automatically detects UTF-8 or CP1252 encoding, validates
        required columns, and ignores empty rows.

        Args:
            file_path: Path to the CSV file to parse.

        Returns:
            List of Player objects parsed from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If required CSV columns are missing or row data is invalid.
            UnicodeDecodeError: If the file cannot be decoded as UTF-8 or CP1252.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Points table file not found: {path}")

        encoding = self._detect_encoding(path)
        _logger.debug("Parsing points table %s using encoding %s", path, encoding)

        with path.open("r", encoding=encoding, newline="") as handle:
            reader = csv.DictReader(handle)
            self._validate_headers(reader.fieldnames, path)
            return [self._parse_row(row, index + 1) for index, row in enumerate(reader) if self._is_non_empty_row(row)]

    def _detect_encoding(self, path: Path) -> str:
        """Detect whether a CSV file is encoded as UTF-8 or CP1252."""
        raw_bytes = path.read_bytes()
        try:
            raw_bytes.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            try:
                raw_bytes.decode("cp1252")
                return "cp1252"
            except UnicodeDecodeError as exc:
                raise UnicodeDecodeError(
                    "utf-8 or cp1252",
                    exc.object,
                    exc.start,
                    exc.end,
                    "Unable to decode file as UTF-8 or CP1252",
                ) from exc

    def _validate_headers(self, headers: Iterable[str] | None, path: Path) -> None:
        """Validate that required CSV headers are present."""
        if headers is None:
            raise ValueError(f"CSV file {path} has no header row.")

        missing = [column for column in self.REQUIRED_COLUMNS if column not in headers]
        if missing:
            raise ValueError(
                f"CSV file {path} is missing required columns: {', '.join(missing)}"
            )

    def _is_non_empty_row(self, row: dict[str, str]) -> bool:
        """Return True if the CSV row contains any non-empty values."""
        return any(value.strip() for value in row.values() if value is not None)

    def _parse_row(self, row: dict[str, str], row_number: int) -> Player:
        """Convert a CSV row into a Player model."""
        try:
            team = row["team"].strip()
            name = row["name"].strip()
            map_points_value = row["map_points"].strip()
        except KeyError as exc:
            raise ValueError(f"Missing required column in row {row_number}: {exc}") from exc

        if not team:
            raise ValueError(f"Empty team value in row {row_number}.")
        if not name:
            raise ValueError(f"Empty player name in row {row_number}.")

        try:
            map_points = [int(value.strip()) for value in map_points_value.split(";") if value.strip()]
        except ValueError as exc:
            raise ValueError(
                f"Invalid map_points format in row {row_number}: {map_points_value}."
            ) from exc

        return Player(team=team, name=name, map_points=map_points)
