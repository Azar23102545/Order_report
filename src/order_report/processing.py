"""Rensning av data och alla beräkningar till rapporterna.

Funktionerna här läser och sparar inga filer, så de är lätta att testa.
"""

import pandas as pd

RETURN_YES_VALUES = ["true", "yes", "1", "ja"]


def _clean_text(column: pd.Series) -> pd.Series:
    """Fyller i saknade värden och gör texten enhetlig, t.ex. ' north' blir 'North'."""
    return column.fillna("Unknown").astype(str).str.strip().str.title()


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Rensar datan på samma sätt som originalprogrammet. Ändrar inte originalet."""
    cleaned = orders.copy()

    cleaned["region"] = _clean_text(cleaned["region"])
    cleaned["product_category"] = _clean_text(cleaned["product_category"])

    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce").fillna(1)

    unit_price = pd.to_numeric(cleaned["unit_price"], errors="coerce")
    cleaned["unit_price"] = unit_price.fillna(unit_price.median())

    cleaned["discount"] = pd.to_numeric(cleaned["discount"], errors="coerce").fillna(0)

    cleaned["returned"] = (
        cleaned["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(RETURN_YES_VALUES)
    )
    return cleaned


def add_order_values(orders: pd.DataFrame) -> pd.DataFrame:
    """Lägger till ordervärde och värde efter rabatt."""
    result = orders.copy()
    result["order_value"] = result["quantity"] * result["unit_price"]
    result["discounted_value"] = result["order_value"] * (1 - result["discount"])
    return result


def create_overview(orders: pd.DataFrame) -> pd.DataFrame:
    """Total försäljning, antal ordrar och antal returer."""
    return pd.DataFrame(
        {
            "metric": ["total_sales", "order_count", "return_count"],
            "value": [
                round(orders["discounted_value"].sum(), 2),
                orders["order_id"].nunique(),
                int(orders["returned"].sum()),
            ],
        }
    )


def summarize_by(orders: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Försäljning och returer per grupp, t.ex. per region eller produktkategori.

    Ersätter de två nästan likadana kodblocken i originalet.
    """
    summary = orders.groupby(group_column, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )
    summary["total_sales"] = summary["total_sales"].round(2)
    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)
    return summary.sort_values("total_sales", ascending=False).reset_index(drop=True)


def summarize_returns(orders: pd.DataFrame) -> pd.DataFrame:
    """Returer per produktkategori, sorterat på högst returgrad först."""
    summary = orders.groupby("product_category", as_index=False).agg(
        order_count=("order_id", "nunique"),
        returns=("returned", "sum"),
    )
    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)
    return summary.sort_values("return_rate", ascending=False).reset_index(drop=True)
