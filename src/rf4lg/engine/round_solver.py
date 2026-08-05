"""Round solver for RF4 League Engine."""

from dataclasses import dataclass, field
from typing import List

from ..models import Match, Player, Round
from .match_solver import MatchSolver


@dataclass(frozen=True)
class RoundSolver:
    """Solve all matches in a round using MatchSolver."""

    match_solver: MatchSolver = field(default_factory=MatchSolver)

    def solve(self, round: Round, players: list[Player]) -> Round:
        """Solve every match in the given round.

        Args:
            round: The round containing matches to solve.
            players: All available players for both teams.

        Returns:
            The updated Round instance with solved matches.
        """
        for index, match in enumerate(round.matches):
            round.matches[index] = self.match_solver.solve(match, players)
        return round
