"""Map solver for RF4 League Engine."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

from ..models import Competition, CompetitionResult, Player


@dataclass(frozen=True)
class MapSolver:
    """Solve a single RF4 competition map between two teams.

    The solver selects up to eight players from each team, sorts by map points,
    and returns a Competition instance with deterministic placement order.
    """

    max_team_players: int = 8
    max_total_players: int = 16

    def solve(
        self,
        home_players: list[Player],
        away_players: list[Player],
        map_name: str,
    ) -> Competition:
        """Solve a single RF4 map and return a Competition object.

        Args:
            home_players: Players available for the home team.
            away_players: Players available for the away team.
            map_name: Name of the map being solved.

        Returns:
            A Competition instance containing ordered CompetitionResult entries.
        """
        selected_home = self._select_team_players(home_players)
        selected_away = self._select_team_players(away_players)

        combined_players = self._combine_teams(selected_home, selected_away)
        ranked_players = self._rank_by_map_points(combined_players)
        results = self._build_results(ranked_players)

        return Competition(
            map_name=map_name,
            start_time=datetime.min,
            results=results,
        )

    def _select_team_players(self, players: list[Player]) -> list[Player]:
        """Select up to max_team_players by descending map points."""
        return sorted(
            players,
            key=self._player_map_points,
            reverse=True,
        )[: self.max_team_players]

    def _combine_teams(
        self,
        home_players: list[Player],
        away_players: list[Player],
    ) -> list[Tuple[Player, str]]:
        """Combine selected home and away players while preserving input order."""
        return [
            (player, "home") for player in home_players
        ] + [
            (player, "away") for player in away_players
        ]

    def _rank_by_map_points(
        self,
        players: list[Tuple[Player, str]],
    ) -> list[Tuple[Player, str]]:
        """Sort players by map points, preserving order on ties."""
        return sorted(
            players,
            key=lambda item: self._player_map_points(item[0]),
            reverse=True,
        )

    def _build_results(
        self,
        ranked_players: list[Tuple[Player, str]],
    ) -> list[CompetitionResult]:
        """Convert ranked players into CompetitionResult objects."""
        return [
            CompetitionResult(position=index + 1, player=player, team=team)
            for index, (player, team) in enumerate(ranked_players[: self.max_total_players])
        ]

    def _player_map_points(self, player: Player) -> int:
        """Return the player's total map points for sorting."""
        return sum(player.map_points)
