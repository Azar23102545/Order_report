"""Sparar rapporterna som CSV-filer."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def save_reports(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Sparar varje rapport som en egen fil. Skapar mappen om den inte finns."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, report in reports.items():
        path = output_dir / filename
        report.to_csv(path, index=False)
        logger.info("Sparade %s", path)
