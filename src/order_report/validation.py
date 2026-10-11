"""Kontroller av att datan ser ut som vi förväntar oss."""

import logging

import pandas as pd

from .config import REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def find_missing_columns(orders: pd.DataFrame) -> list[str]:
    """Returnerar de obligatoriska kolumner som saknas, i bokstavsordning."""
    return sorted(REQUIRED_COLUMNS - set(orders.columns))


def validate_orders(orders: pd.DataFrame) -> None:
    """Stoppar programmet om datan saknar kolumner eller rader."""
    missing = find_missing_columns(orders)
    if missing:
        raise ValueError(f"Obligatoriska kolumner saknas: {', '.join(missing)}")

    if orders.empty:
        raise ValueError("Datan innehåller inga rader")

    logger.info("Validering klar, alla obligatoriska kolumner finns")


def warn_about_bad_values(orders: pd.DataFrame) -> None:
    """Loggar varningar för värden som programmet måste fylla i eller rätta."""
    for column in ["quantity", "unit_price", "discount"]:
        not_numeric = pd.to_numeric(orders[column], errors="coerce").isna().sum()
        if not_numeric:
            logger.warning("%d rader i %s saknas eller är inte siffror", not_numeric, column)

    for column in ["region", "product_category"]:
        missing = orders[column].isna().sum()
        if missing:
            logger.warning("%d rader saknar %s och sätts till Unknown", missing, column)
