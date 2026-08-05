"""Match point calculation for RF4 League Engine."""

from typing import Dict, List

from .models import CompetitionResult
from .logger import get_logger

_logger = get_logger(__name__)


class MatchPoints:
    """Calculate team points based on competition placements."""

    POINTS_BY_POSITION = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    def calculate(self, placements: List[CompetitionResult]) -> Dict[str, int]:
        """Calculate match points for home and away teams.

        Args:
            placements: A list of CompetitionResult objects ordered by position.

        Returns:
            A dictionary containing total points for the home and away teams.
        """
        totals = {"home": 0, "away": 0}

        for index, placement in enumerate(placements):
            if index >= len(self.POINTS_BY_POSITION):
                break

            points = self.POINTS_BY_POSITION[index]
            if placement.team not in totals:
                _logger.debug(
                    "Skipping unknown team %s at position %d.",
                    placement.team,
                    placement.position,
                )
                continue

            totals[placement.team] += points

        _logger.info(
            "Calculated match points: home=%d, away=%d.",
            totals["home"],
            totals["away"],
        )
        return totals
