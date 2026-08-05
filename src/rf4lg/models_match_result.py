"""Match result models for RF4 League Engine."""

from dataclasses import dataclass
from typing import List

from .models import Competition, Match


@dataclass
class MatchResult:
    """Represent the result of a match including competition details."""

    match: Match
    competitions: List[Competition]
    home_map_points: List[int]
    away_map_points: List[int]
