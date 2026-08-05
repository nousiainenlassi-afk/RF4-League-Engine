"""Generation utilities for RF4 League Engine."""

import logging
from pathlib import Path
from typing import List

from .formatter import RF4Formatter
from .logger import get_logger
from .models import Competition, CompetitionResult, Player, Season
from .parser import PointsTableParser
from .scheduler import ScheduleLoader

_logger = get_logger(__name__)


class RoundGenerator:
    """Generate RF4 competition log text for a league round."""

    def __init__(
        self,
        schedule_loader: ScheduleLoader,
        points_parser: PointsTableParser,
        formatter: RF4Formatter,
    ) -> None:
        self.schedule_loader = schedule_loader
        self.points_parser = points_parser
        self.formatter = formatter

    def generate_round(self, season: str, round_number: int, points_path: Path | str) -> str:
        """Generate formatted output for a season round.

        The method loads the schedule and points table, maps players to teams,
        creates competition results based on total points, and returns a formatted
        RF4 competition log.

        Args:
            season: Season identifier matching the schedule directory.
            round_number: Round number to generate.
            points_path: Path to the points CSV file.

        Returns:
            Generated competition text for the requested round.
        """
        season_model = self.schedule_loader.load(season)
        round_model = self._get_round(season_model, round_number)
        players = self.points_parser.parse(points_path)

        _logger.debug(
            "Loaded schedule for season %s round %d and %d players from points table.",
            season,
            round_number,
            len(players),
        )

        competitions_text: List[str] = []
        for match in round_model.matches:
            for scheduled_competition in match.competitions:
                results = self._build_results(match, players)
                competition = Competition(
                    map_name=scheduled_competition.map_name,
                    start_time=scheduled_competition.start_time,
                    results=results,
                )
                competitions_text.append(
                    self.formatter.format_competition(
                        map_name=competition.map_name,
                        start_time=competition.start_time,
                        results=competition.results,
                        biggest_fish=None,
                    )
                )

        return "\n\n".join(competitions_text)

    def _get_round(self, season_model: Season, round_number: int) -> "Round":
        """Retrieve the requested round from the season model."""
        if round_number not in season_model.rounds:
            raise ValueError(f"Round {round_number} not found in season {season_model.name}.")
        return season_model.rounds[round_number]

    def _build_results(self, match: "Match", players: List[Player]) -> List[CompetitionResult]:
        """Build placeholder competition results ordered by player total points."""
        eligible_players = [
            player for player in players if player.team in {match.home_team, match.away_team}
        ]

        sorted_players = sorted(eligible_players, key=lambda player: player.total_points, reverse=True)
        return [CompetitionResult(position=index + 1, player=player) for index, player in enumerate(sorted_players)]
