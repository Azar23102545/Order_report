"""Inställningar för programmet, till exempel var filerna ligger."""

from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
}


@dataclass(frozen=True)
class ReportConfig:
    """Sökvägar till indata och mappen där rapporterna sparas."""

    input_path: Path = Path("data/orders.csv")
    output_dir: Path = Path("output")
