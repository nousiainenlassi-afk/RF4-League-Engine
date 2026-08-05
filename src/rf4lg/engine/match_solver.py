"""Match solver for RF4 League Engine."""

from dataclasses import dataclass, field
from datetime import datetime

from ..models import Competition, Match, Player
from .map_solver import MapSolver


@dataclass(frozen=True)
class MatchSolver:
    """Solve a single RF4 match by generating three map competitions."""

    map_solver: MapSolver = field(default_factory=MapSolver)

    def solve(self, match: Match, players: list[Player]) -> Match:
        """Solve a match by splitting players by team and producing three competitions.

        Args:
            match: The match to solve.
            players: All available players for both teams.

        Returns:
            The updated Match instance with three Competition objects.
        """
        home_players, away_players = self._split_players_by_team(players, match.home_team, match.away_team)

        competitions = [
            self.map_solver.solve(home_players, away_players, f"Map {map_number}")
            for map_number in range(1, 4)
        ]

        match.competitions = competitions
        return match

    def _split_players_by_team(
        self,
        players: list[Player],
        home_team: str,
        away_team: str,
    ) -> tuple[list[Player], list[Player]]:
        """Split all players into home and away teams."""
        home_players: list[Player] = []
        away_players: list[Player] = []

        for player in players:
            if player.team == home_team:
                home_players.append(player)
            elif player.team == away_team:
                away_players.append(player)

        return home_players, away_players
