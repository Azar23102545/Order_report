import pandas as pd
import pytest

from order_report.processing import (
    add_order_values,
    clean_orders,
    create_overview,
    summarize_by,
    summarize_returns,
)


@pytest.fixture
def orders():
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "region": [" north", "North", None, "South"],
            "product_category": ["books", "Books", "Toys", "toys "],
            "quantity": [2, "abc", 1, None],
            "unit_price": [100.0, 50.0, None, 10.0],
            "discount": [0.1, 0, None, 0.5],
            "returned": ["yes", "no", None, "JA"],
        }
    )


def test_clean_orders_fixes_text(orders):
    cleaned = clean_orders(orders)
    assert list(cleaned["region"]) == ["North", "North", "Unknown", "South"]
    assert list(cleaned["product_category"]) == ["Books", "Books", "Toys", "Toys"]


def test_clean_orders_fills_missing_numbers(orders):
    cleaned = clean_orders(orders)
    assert list(cleaned["quantity"]) == [2, 1, 1, 1]
    assert cleaned.loc[2, "unit_price"] == 50.0  # medianen av 100, 50 och 10
    assert cleaned.loc[2, "discount"] == 0


def test_clean_orders_reads_returned_values(orders):
    cleaned = clean_orders(orders)
    assert list(cleaned["returned"]) == [True, False, False, True]


def test_clean_orders_does_not_change_original(orders):
    original = orders.copy()
    clean_orders(orders)
    pd.testing.assert_frame_equal(orders, original)


def test_add_order_values():
    df = pd.DataFrame({"quantity": [2, 3], "unit_price": [100.0, 10.0], "discount": [0.1, 0.0]})
    result = add_order_values(df)
    assert list(result["order_value"]) == [200.0, 30.0]
    assert result["discounted_value"].tolist() == pytest.approx([180.0, 30.0])


def test_overview(orders):
    data = add_order_values(clean_orders(orders))
    overview = create_overview(data).set_index("metric")["value"]
    assert overview["total_sales"] == pytest.approx(180 + 50 + 50 + 5)
    assert overview["order_count"] == 4
    assert overview["return_count"] == 2


def test_summarize_by_region(orders):
    data = add_order_values(clean_orders(orders))
    summary = summarize_by(data, "region")
    north = summary[summary["region"] == "North"].iloc[0]
    assert north["order_count"] == 2
    assert north["total_sales"] == pytest.approx(230.0)
    assert north["return_rate"] == 0.5
    assert summary.iloc[0]["region"] == "North"  # sorterad på försäljning


def test_summarize_returns_sorted_by_rate(orders):
    data = add_order_values(clean_orders(orders))
    summary = summarize_returns(data)
    assert list(summary["return_rate"]) == [0.5, 0.5]
    assert set(summary["product_category"]) == {"Books", "Toys"}
