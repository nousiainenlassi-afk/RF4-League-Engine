"""Solver logic for RF4 League Engine."""

from typing import List

from ..logger import get_logger
from ..models import CompetitionResult, Player

_logger = get_logger(__name__)


class RankingSolver:
    """Solve match rankings based on player total points."""

    def solve_match(
        self,
        home_players: List[Player],
        away_players: List[Player],
    ) -> List[CompetitionResult]:
        """Produce a deterministic ranking for a match between two teams.

        Args:
            home_players: Players available for the home team.
            away_players: Players available for the away team.

        Returns:
            A list of 16 CompetitionResult objects ordered by position.
        """
        selected_home = sorted(home_players, key=lambda player: player.total_points, reverse=True)[:8]
        selected_away = sorted(away_players, key=lambda player: player.total_points, reverse=True)[:8]

        combined: List[tuple[Player, str]] = [
            (player, "home") for player in selected_home
        ] + [
            (player, "away") for player in selected_away
        ]
        ranked = sorted(combined, key=lambda item: item[0].total_points, reverse=True)

        results: List[CompetitionResult] = [
            CompetitionResult(position=index + 1, player=player, team=team)
            for index, (player, team) in enumerate(ranked[:16])
        ]

        if len(results) < 16:
            _logger.warning(
                "RankingSolver produced %d results; expected 16."
                " Missing player slots were not filled.",
                len(results),
            )

        return results
