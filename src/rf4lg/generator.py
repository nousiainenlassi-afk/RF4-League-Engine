"""Generation utilities for RF4 League Engine."""

from pathlib import Path
from typing import Iterable

from .models import Season, Match


def generate_output(season: Season, output_dir: Path | str) -> Path:
    """Generate output files for the season."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    output_path = path / f"season_{season.year}.txt"
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(f"Season: {season.year}\n")
        output_file.write(f"Teams: {len(season.teams)}\n\n")
        for match in season.matches:
            output_file.write(format_match(match) + "\n")

    return output_path


def format_match(match: Match) -> str:
    """Render a single match as plain text."""
    return (
        f"{match.date} - {match.home_team.name} vs {match.away_team.name}"
        f" @ {match.venue}"
    )
