"""Domain models for RF4 League Engine."""

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Team:
    id: int
    name: str
    coach: str | None = None


@dataclass
class Match:
    home_team: Team
    away_team: Team
    date: date
    venue: str
    score_home: int | None = None
    score_away: int | None = None


@dataclass
class Season:
    year: str
    teams: List[Team]
    matches: List[Match]
