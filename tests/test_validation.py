import pandas as pd
import pytest

from order_report.config import REQUIRED_COLUMNS
from order_report.loading import load_orders
from order_report.validation import find_missing_columns, validate_orders


def make_orders(rows=1):
    return pd.DataFrame({column: [1] * rows for column in REQUIRED_COLUMNS})


def test_valid_data_passes():
    validate_orders(make_orders())


def test_missing_column_is_named_in_error():
    orders = make_orders().drop(columns=["discount", "region"])
    assert find_missing_columns(orders) == ["discount", "region"]
    with pytest.raises(ValueError, match="discount, region"):
        validate_orders(orders)


def test_empty_data_is_rejected():
    with pytest.raises(ValueError, match="inga rader"):
        validate_orders(make_orders(rows=0))


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_orders(tmp_path / "finns_inte.csv")


def test_empty_file(tmp_path):
    path = tmp_path / "tom.csv"
    path.write_text("")
    with pytest.raises(ValueError, match="tom"):
        load_orders(path)
