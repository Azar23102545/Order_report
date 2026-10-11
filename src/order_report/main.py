"""Startpunkt för programmet. Kör med: python -m order_report"""

import logging

from .config import ReportConfig
from .loading import load_orders
from .processing import add_order_values, clean_orders, create_overview, summarize_by, summarize_returns
from .reporting import save_reports
from .validation import validate_orders, warn_about_bad_values

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def run(config: ReportConfig) -> None:
    """Hela flödet: läs in, validera, rensa, räkna och spara."""
    orders = load_orders(config.input_path)
    validate_orders(orders)
    warn_about_bad_values(orders)

    orders = add_order_values(clean_orders(orders))

    reports = {
        "overview.csv": create_overview(orders),
        "sales_by_category.csv": summarize_by(orders, "product_category"),
        "sales_by_region.csv": summarize_by(orders, "region"),
        "returns_by_category.csv": summarize_returns(orders),
    }
    save_reports(reports, config.output_dir)


def main() -> int:
    setup_logging()
    logger.info("Startar orderrapport")

    try:
        run(ReportConfig())
    except (FileNotFoundError, ValueError) as error:
        logger.error("Rapporten kunde inte skapas: %s", error)
        return 1
    except Exception:
        logger.exception("Oväntat fel i programmet")
        return 1

    logger.info("Klart")
    return 0
