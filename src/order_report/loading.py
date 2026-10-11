"""Läser in orderdata från fil."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_orders(path: Path) -> pd.DataFrame:
    """Läser CSV-filen och ger tydliga fel om filen saknas eller är tom."""
    if not path.exists():
        raise FileNotFoundError(f"Hittar inte datafilen: {path}")

    try:
        orders = pd.read_csv(path)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"Datafilen är tom: {path}") from error

    logger.info("Läste in %d rader från %s", len(orders), path)
    return orders
