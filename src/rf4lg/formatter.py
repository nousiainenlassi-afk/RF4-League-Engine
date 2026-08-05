"""Formatting utilities for RF4 League Engine."""

from datetime import datetime
from typing import List

from .models import CompetitionResult


class RF4Formatter:
    """Format RF4 competition and result messages."""

    def format_competition_start(self, map_name: str, start_time: datetime) -> str:
        """Format the start notification for a competition."""
        timestamp = start_time.strftime("%d.%m.%Y %H:%M")
        return f"New LAN CLIENT competition started: {map_name}. [{timestamp}]"

    def format_results(self, results: List[CompetitionResult]) -> str:
        """Format competition results into a ranked text block."""
        lines = ["Competition finished. Results:"]
        for index, result in enumerate(results, start=1):
            lines.append(f"{index}. [{result.player.team}] {result.player.name}")
        return "\n".join(lines)

    def format_biggest_fish(self, player_name: str) -> str:
        """Format the biggest fish announcement."""
        return f"Biggest fish:\n{player_name}"
