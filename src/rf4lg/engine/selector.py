"""Team selection logic for RF4 League Engine."""

from typing import List

from ..logger import get_logger
from ..models import Player

_logger = get_logger(__name__)


class TeamSelector:
    """Select players for a match by team and score."""

    def select_players(self, players: List[Player], team_name: str) -> List[Player]:
        """Return the top players from a single team for a match.

        Args:
            players: All available players.
            team_name: Name of the team to select players for.

        Returns:
            Selected Player objects for the team.
        """
        filtered_players = [player for player in players if player.team == team_name]
        _logger.debug(
            "Selected %d players for team %s before sorting.",
            len(filtered_players),
            team_name,
        )

        sorted_players = sorted(
            filtered_players,
            key=lambda player: player.total_points,
            reverse=True,
        )
        selected_players = sorted_players[:8]

        _logger.info(
            "Team %s selection complete. Returning %d players.",
            team_name,
            len(selected_players),
        )
        return selected_players
