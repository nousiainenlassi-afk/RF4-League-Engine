"""Map building utilities for RF4 League Engine."""

from __future__ import annotations

from typing import Dict, List

from ..models import Player


class MapBuilder:
    """Build map-specific player lists from raw player data."""

    MAP_KEYS = ["map1", "map2", "map3"]

    def build(self, players: List[Player]) -> Dict[str, List[Player]]:
        """Build map-specific player groups from provided players.

        Each returned map contains only players who scored more than zero
        points for that map. The players in each map list are sorted by map
        points in descending order while preserving original order when points
        are tied.

        Args:
            players: A list of Player objects with per-map points.

        Returns:
            A dictionary with keys "map1", "map2", and "map3".
        """
        maps: Dict[str, List[Player]] = {}

        for index, key in enumerate(self.MAP_KEYS):
            filtered_players = [
                player for player in players if player.map_points[index] > 0
            ]
            sorted_players = sorted(
                filtered_players,
                key=lambda player: player.map_points[index],
                reverse=True,
            )
            maps[key] = sorted_players

        return maps
