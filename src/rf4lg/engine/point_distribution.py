"""Point distribution utilities for RF4 League Engine."""

from __future__ import annotations

from typing import List, Tuple


class PointDistributionGenerator:
    """Generate valid point distributions for a fixed total."""

    MIN_POINT = 0
    MAX_POINT = 10
    DISTRIBUTION_SIZE = 3

    def generate(self, total_points: int) -> List[Tuple[int, int, int]]:
        """Return all unique distributions of three point values.

        Each distribution consists of three integers between 0 and 10,
        inclusive, and the values sum to the provided total_points.

        The returned tuples are sorted in descending order, and duplicate
        value permutations are collapsed so that each combination appears
        only once.

        Args:
            total_points: Total number of points to distribute.

        Returns:
            A list of unique descending point tuples.
        """
        valid_distributions: set[Tuple[int, int, int]] = set()

        for first in range(self.MIN_POINT, self.MAX_POINT + 1):
            for second in range(self.MIN_POINT, self.MAX_POINT + 1):
                for third in range(self.MIN_POINT, self.MAX_POINT + 1):
                    if first + second + third != total_points:
                        continue

                    distribution = tuple(sorted((first, second, third), reverse=True))
                    valid_distributions.add(distribution)

        return sorted(valid_distributions, reverse=True)
