"""Map solver for RF4 League Engine."""

from dataclasses import dataclass
from typing import List, Tuple

from ..models import CompetitionResult, Player


@dataclass(frozen=True)
class MapSolver:
    """Solve a single RF4 competition map between two teams.

    The solver selects up to eight players from each team, maintains the
    original order for tied map-point totals, and assigns placements from
    1 to 16.
    """

    max_team_players: int = 8
    max_total_players: int = 16

    def solve_map(
        self,
        home_players: List[Player],
        away_players: List[Player],
    ) -> List[CompetitionResult]:
        """Solve a single map and return ordered competition results.

        Args:
            home_players: Players available for the home team.
            away_players: Players available for the away team.

        Returns:
            A list of CompetitionResult objects ordered by map points.
        """
        selected_home = self._select_top_team_players(home_players)
        selected_away = self._select_top_team_players(away_players)

        combined = self._combine_teams(selected_home, selected_away)
        ranked = self._rank_by_map_points(combined)

        return self._assign_positions(ranked)

    def _select_top_team_players(self, players: List[Player]) -> List[Player]:
        """Select up to max_team_players by descending map points."""
        return sorted(
            players,
            key=self._map_points_score,
            reverse=True,
        )[: self.max_team_players]

    def _combine_teams(
        self,
        home_players: List[Player],
        away_players: List[Player],
    ) -> List[Tuple[Player, str]]:
        """Combine home and away players while preserving team origin."""
        return [(player, "home") for player in home_players] + [
            (player, "away") for player in away_players
        ]

    def _rank_by_map_points(
        self,
        players: List[Tuple[Player, str]],
    ) -> List[Tuple[Player, str]]:
        """Sort players by total map points, preserving input order on ties."""
        return sorted(
            players,
            key=lambda item: self._map_points_score(item[0]),
            reverse=True,
        )

    def _assign_positions(
        self,
        ranked_players: List[Tuple[Player, str]],
    ) -> List[CompetitionResult]:
        """Assign 1..max_total_players positions to the ranked players."""
        results: List[CompetitionResult] = []
        for index, (player, team) in enumerate(ranked_players[: self.max_total_players]):
            results.append(
                CompetitionResult(
                    position=index + 1,
                    player=player,
                    team=team,
                )
            )
        return results

    def _map_points_score(self, player: Player) -> int:
        """Return the total map points score for a player."""
        return sum(player.map_points)
