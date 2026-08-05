"""Round generation for RF4 League Engine."""

from pathlib import Path
from typing import List

from ..formatter import RF4Formatter
from ..logger import get_logger
from ..models import CompetitionResult, Match, Player, Round, Season
from ..parser import PointsTableParser
from ..scheduler import ScheduleLoader
from .selector import TeamSelector
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
        team_selector: TeamSelector,
    ) -> None:
        self.schedule_loader = schedule_loader
        self.points_parser = points_parser
        self.formatter = formatter
        self.ranking_solver = ranking_solver
        self.team_selector = team_selector

    def generate_round(self, season: str, round_number: int, points_path: Path | str) -> str:
        """Generate formatted output for a season round.

        The method loads the requested round schedule, loads all players, selects
        players for each team, ranks the match using RankingSolver, and formats
        each competition into combined round text.

        Args:
            season: Season identifier matching the schedule directory.
            round_number: Round number to generate.
            points_path: Path to the points CSV file.

        Returns:
            Generated text for the complete round.
        """
        season_model = self._load_schedule(season)
        round_model = self._get_round(season_model, round_number)
        players = self._load_players(points_path)

        _logger.info(
            "Generating round %d for season %s with %d players.",
            round_number,
            season,
            len(players),
        )

        competition_texts: List[str] = []
        for match in round_model.matches:
            _logger.info(
                "Processing match: %s vs %s", match.home_team, match.away_team
            )
            home_players = self.team_selector.select_players(players, match.home_team)
            away_players = self.team_selector.select_players(players, match.away_team)
            results = self.ranking_solver.solve_match(home_players, away_players)

            _logger.debug(
                "Ranked %d players for match: %s vs %s.",
                len(results),
                match.home_team,
                match.away_team,
            )

            competition_texts.extend(self._format_match_competitions(match, results))

        return "\n\n".join(competition_texts)

    def _load_schedule(self, season: str) -> Season:
        _logger.debug("Loading schedule for season %s", season)
        return self.schedule_loader.load(season)

    def _load_players(self, points_path: Path | str) -> List[Player]:
        _logger.debug("Loading players from points path %s", points_path)
        return self.points_parser.parse(points_path)

    def _format_match_competitions(self, match: Match, results: List[CompetitionResult]) -> List[str]:
        texts: List[str] = []
        for competition_schedule in match.competitions:
            _logger.debug(
                "Formatting competition %s for match %s vs %s.",
                competition_schedule.map_name,
                match.home_team,
                match.away_team,
            )
            texts.append(
                self.formatter.format_competition(
                    map_name=competition_schedule.map_name,
                    start_time=competition_schedule.start_time,
                    results=results,
                    biggest_fish=None,
                )
            )
        return texts

    def _get_round(self, season_model: Season, round_number: int) -> Round:
        if round_number not in season_model.rounds:
            raise ValueError(f"Round {round_number} not found in season {season_model.name}.")
        return season_model.rounds[round_number]
