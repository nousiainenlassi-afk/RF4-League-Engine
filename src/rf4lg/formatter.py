"""Formatting utilities for RF4 League Engine."""

from datetime import datetime
from typing import List

from .models import CompetitionResult


class RF4Formatter:
    """Format RF4 LAN competition logs from competition data."""

    def format_header(self, map_name: str, start_time: datetime) -> str:
        """Return the RF4 competition start line."""
        timestamp = start_time.strftime("%d.%m.%Y %H:%M")
        return f"New LAN CLIENT competition started: {map_name}. [{timestamp}]"

    def format_results(self, results: List[CompetitionResult]) -> str:
        """Return the RF4 competition results block."""
        lines = ["Competition finished. Results:"]
        for index, result in enumerate(results, start=1):
            lines.append(f"{index}. [{result.player.team}] {result.player.name}")
        return "\n".join(lines)

    def format_biggest_fish(self, player_name: str | None) -> str:
        """Return the RF4 biggest fish block or an empty string."""
        if player_name is None:
            return ""
        return f"Biggest fish:\n{player_name}"

    def format_competition(
        self,
        map_name: str,
        start_time: datetime,
        results: List[CompetitionResult],
        biggest_fish: str | None,
    ) -> str:
        """Return a complete RF4 competition log entry."""
        lines = [self.format_header(map_name, start_time), self.format_results(results)]
        biggest_fish_block = self.format_biggest_fish(biggest_fish)
        if biggest_fish_block:
            lines.append(biggest_fish_block)
        return "\n".join(lines)
