"""Entry point for the RF4 League Engine command line application."""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

from .config import Config
from .formatter import RF4Formatter
from .io import OutputWriter
from .logger import get_logger
from .parser import PointsTableParser
from .scheduler import ScheduleLoader
from .solver import RankingSolver
from .generator import RoundGenerator

_logger = get_logger(__name__)


class Main:
    """Command line application for loading RF4 league schedules and points."""

    def __init__(
        self,
        config: Config,
        parser: PointsTableParser,
        schedule_loader: ScheduleLoader,
        round_generator: RoundGenerator,
        output_writer: OutputWriter,
    ) -> None:
        self.config = config
        self.parser = parser
        self.schedule_loader = schedule_loader
        self.round_generator = round_generator
        self.output_writer = output_writer

    def run(self, season: str, round_number: int, points_path: Path) -> int:
        """Execute the main application logic.

        Args:
            season: Season identifier to load.
            round_number: Round number to validate and load.
            points_path: Path to the points CSV file.

        Returns:
            Exit code indicating success.
        """
        self._validate_round(round_number)
        self._validate_points_path(points_path)

        output_text = self.round_generator.generate_round(season, round_number, points_path)
        output_file = self.output_writer.write_round(round_number, output_text, Path("output"))

        _logger.info("Round generated successfully: %s", output_file)
        return 0

    def _validate_round(self, round_number: int) -> None:
        """Validate that the round number is a positive integer."""
        if round_number < 1:
            raise ValueError("Round must be a positive integer.")

    def _validate_points_path(self, path: Path) -> None:
        """Validate that the points CSV file exists."""
        if not path.exists():
            raise FileNotFoundError(f"Points file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Points path is not a file: {path}")


def parse_args(argv: Optional[list[str]] = None) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="RF4 League Engine command line interface.")
    parser.add_argument("--season", required=True, help="Season identifier to load.")
    parser.add_argument("--round", required=True, type=int, help="Round number to load.")
    parser.add_argument("--points", required=True, help="Path to the points CSV file.")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point for the RF4 League Engine application."""
    args = parse_args(argv)
    config = Config()
    points_parser = PointsTableParser()
    schedule_loader = ScheduleLoader()
    formatter = RF4Formatter()
    ranking_solver = RankingSolver()
    round_generator = RoundGenerator(
        schedule_loader=schedule_loader,
        points_parser=points_parser,
        formatter=formatter,
        ranking_solver=ranking_solver,
    )
    output_writer = OutputWriter()

    app = Main(
        config=config,
        parser=points_parser,
        schedule_loader=schedule_loader,
        round_generator=round_generator,
        output_writer=output_writer,
    )
    return app.run(args.season, args.round, Path(args.points))


if __name__ == "__main__":
    raise SystemExit(main())
