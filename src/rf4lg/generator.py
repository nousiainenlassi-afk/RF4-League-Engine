"""Generation utilities for RF4 League Engine."""

from pathlib import Path
from typing import Dict, List

from .formatter import RF4Formatter
from .logger import get_logger
from .models import Competition, CompetitionResult, Match, Player, Round, Season
from .parser import PointsTableParser
from .scheduler import ScheduleLoader
from .solver import RankingSolver

_logger = get_logger(__name__)


class RoundGenerator:
    """Generate RF4 competition log text for a league round."""

    def __init__(
        self,
        schedule_loader: ScheduleLoader,
        points_parser: PointsTableParser,
        formatter: RF4Formatter,
        ranking_solver: RankingSolver,
    ) -> None:
        self.schedule_loader = schedule_loader
        self.points_parser = points_parser
        self.formatter = formatter
        self.ranking_solver = ranking_solver

    def generate_round(self, season: str, round_number: int, points_path: Path | str) -> str:
        """Generate formatted output for a season round.

        The method loads the schedule and points table, groups players by team,
        uses RankingSolver to rank each match, and returns a complete formatted
        RF4 competition log for the requested round.

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
        players_by_team = self._group_players_by_team(players)

        _logger.debug(
            "Loaded schedule for season %s round %d and %d players from points table.",
            season,
            round_number,
            len(players),
        )

        competitions_text: List[str] = []
        for match in round_model.matches:
            home_players = players_by_team.get(match.home_team, [])
            away_players = players_by_team.get(match.away_team, [])

            _logger.debug(
                "Building results for match %s vs %s with %d home and %d away players.",
                match.home_team,
                match.away_team,
                len(home_players),
                len(away_players),
            )

            results = self.ranking_solver.solve_match(home_players, away_players)
            for competition_schedule in match.competitions:
                competitions_text.append(
                    self.formatter.format_competition(
                        map_name=competition_schedule.map_name,
                        start_time=competition_schedule.start_time,
                        results=results,
                        biggest_fish=None,
                    )
                )

        return "\n\n".join(competitions_text)

    def _group_players_by_team(self, players: List[Player]) -> Dict[str, List[Player]]:
        """Group parsed players by their team name."""
        grouped: Dict[str, List[Player]] = {}
        for player in players:
            grouped.setdefault(player.team, []).append(player)
        return grouped

    def _get_round(self, season_model: Season, round_number: int) -> Round:
        """Retrieve the requested round from the season model."""
        if round_number not in season_model.rounds:
            raise ValueError(f"Round {round_number} not found in season {season_model.name}.")
        return season_model.rounds[round_number]
