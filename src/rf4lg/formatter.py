"""Formatting helpers for RF4 League Engine."""

from pathlib import Path
from typing import Sequence

from .models import Match, Season


def format_season_summary(season: Season) -> str:
    """Return a formatted summary of the season."""
    lines = [f"Season: {season.year}", f"Teams: {len(season.teams)}", "Matches:"]
    for match in season.matches:
        lines.append(format_match(match))
    return "\n".join(lines)


def format_match(match: Match) -> str:
    """Format a single match into a human-readable string."""
    return (
        f"{match.date.isoformat()} | {match.home_team.name} vs {match.away_team.name}"
        f" | Venue: {match.venue}"
    )


def write_summary(summary: str, output_path: Path | str) -> Path:
    """Write formatted summary text to a file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(summary, encoding="utf-8")
    return path
