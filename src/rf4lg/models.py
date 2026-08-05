"""Domain models for RF4 League Engine."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Player:
    """Represent a player competing in RF4 League events."""

    team: str
    name: str
    map_points: list[int]


@dataclass
class CompetitionResult:
    """Represent a single competition result for a player."""

    position: int
    player: Player
    biggest_fish: bool = False


@dataclass
class Competition:
    """Represent a competition held on a specific map."""

    map_name: str
    start_time: datetime
    results: list[CompetitionResult]


@dataclass
class Match:
    """Represent a match between two teams."""

    home_team: str
    away_team: str
    competitions: list[Competition]


@dataclass
class Round:
    """Represent a round of matches in a season."""

    number: int
    matches: list[Match]


@dataclass
class Season:
    """Represent a league season composed of sequential rounds."""

    name: str
    rounds: dict[int, Round]
