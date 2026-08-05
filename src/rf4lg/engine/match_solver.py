"""Match solver for RF4 League Engine."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from ..models import Competition, CompetitionResult, Player
from .map_solver import MapSolver


@dataclass(frozen=True)
class MatchSolver:
    """Solve a single RF4 match consisting of three competition maps."""

    map_solver: MapSolver = field(default_factory=MapSolver)

    def solve_match(
        self,
        home_players: List[Player],
        away_players: List[Player],
    ) -> List[Competition]:
        """Solve a match through map 1, map 2 and map 3.

        Args:
            home_players: Players available for the home team.
            away_players: Players available for the away team.

        Returns:
            A list of three Competition objects, one for each map.
        """
        competitions: List[Competition] = []
        for map_number in range(1, 4):
            results: List[CompetitionResult] = self.map_solver.solve_map(
                home_players, away_players
            )
            competitions.append(
                Competition(
                    map_name=f"Map {map_number}",
                    start_time=datetime.min,
                    results=results,
                )
            )

        return competitions
