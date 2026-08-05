"""Scheduling logic for RF4 League Engine."""

from datetime import date, timedelta
from typing import List

from .models import Match, Season


def build_schedule(season: Season, start_date: date, interval_days: int = 7) -> List[Match]:
    """Generate a basic round-robin schedule for the season."""
    matches: List[Match] = []
    teams = season.teams
    if len(teams) < 2:
        return matches

    current_date = start_date
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            matches.append(
                Match(
                    home_team=teams[i],
                    away_team=teams[j],
                    date=current_date,
                    venue="TBD",
                )
            )
            current_date += timedelta(days=interval_days)

    season.matches = matches
    return matches
