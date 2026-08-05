"""Formatting utilities for RF4 League Engine."""

from datetime import datetime
from typing import List

from .models import Competition, CompetitionResult


class RF4Formatter:
    """Format RF4 competition logs and result messages."""

    def format_start(self, map_name: str, start_time: datetime) -> str:
        """Format the competition start log entry."""
        timestamp = start_time.strftime("%d.%m.%Y %H:%M")
        return f"New LAN CLIENT competition started: {map_name}. [{timestamp}]"

    def format_results(self, results: List[CompetitionResult]) -> str:
        """Format competition results into ranked output."""
        lines = ["Competition finished. Results:"]
        for index, result in enumerate(results, start=1):
            lines.append(f"{index}. [{result.player.team}] {result.player.name}")
        return "\n".join(lines)

    def format_biggest_fish(self, player_name: str) -> str:
        """Format the biggest fish announcement."""
        return f"Biggest fish:\n{player_name}"

    def format_competition(self, competition: Competition) -> str:
        """Format an entire competition log entry."""
        lines = [self.format_start(competition.map_name, competition.start_time), self.format_results(competition.results)]

        biggest_fish_player = self._find_biggest_fish(competition.results)
        if biggest_fish_player is not None:
            lines.append(self.format_biggest_fish(biggest_fish_player))

        return "\n".join(lines)

    def _find_biggest_fish(self, results: List[CompetitionResult]) -> str | None:
        """Return the player name with the biggest fish flag, if any."""
        for result in results:
            if result.biggest_fish:
                return result.player.name
        return None
