"""Domain models for RF4 League Engine."""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Player:
    """Represent a player participating in the RF4 League."""

    team: str
    name: str
    map_points: List[int]


@dataclass
class Match:
    """Represent a league match and its map-level results."""

    home_team: str
    away_team: str
    maps: List[str]
    result: str
    map_scores: List[str]


@dataclass
class Competition:
    """Represent a single competition in a round."""

    map_name: str
    datetime: datetime
    placements: List
    biggest_fish: str | None = None


@dataclass
class Round:
    """Represent a competition round within a season."""

    number: int
    competitions: List[Competition]


@dataclass
class Season:
    """Represent a full league season composed of rounds."""

    name: str
    rounds: dict[int, Round]
