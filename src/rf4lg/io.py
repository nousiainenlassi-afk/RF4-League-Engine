"""I/O utilities for RF4 League Engine."""

from pathlib import Path
from typing import Optional

from .logger import get_logger

_logger = get_logger(__name__)


class OutputWriter:
    """Write generated round output to disk."""

    def write_round(self, round_number: int, content: str, output_directory: Path) -> Path:
        """Write the provided round content to a file in the output directory.

        The output file is named using two-digit round numbering and saved with
        UTF-8 encoding.

        Args:
            round_number: The round number to include in the filename.
            content: The text content to write to the file.
            output_directory: Directory where the output file will be created.

        Returns:
            The Path to the created output file.
        """
        output_directory.mkdir(parents=True, exist_ok=True)
        filename = f"Kierros{round_number:02d}.txt"
        output_path = output_directory / filename

        _logger.debug("Writing round %d output to %s", round_number, output_path)
        output_path.write_text(content, encoding="utf-8")

        _logger.info("Wrote round output to %s", output_path)
        return output_path
