from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest

from .demo_data import generate_demo_dataset

REQUIRED_COLUMNS = {
    "transaction_id", "transaction_date", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "discount_pct",
}


@dataclass
class RetailAnalytics:
    data_path: Path

    def load(self) -> pd.DataFrame:
        if not self.data_path.exists():
            generate_demo_dataset(self.data_path)
        frame = pd.read_csv(self.data_path)
        missing = REQUIRED_COLUMNS.difference(frame.columns)
        if missing:
            raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
        frame["transaction_date"] = pd.to_datetime(frame["transaction_date"], errors="raise")
        for column in ("quantity", "unit_price", "discount_pct"):
            frame[column] = pd.to_numeric(frame[column], errors="raise")
        if (frame["quantity"] <= 0).any() or (frame["unit_price"] < 0).any():
            raise ValueError("Quantity must be positive and unit price cannot be negative.")
        frame["revenue"] = frame["quantity"] * frame["unit_price"] * (1 - frame["discount_pct"])
        return frame

    def overview(self) -> dict:
        frame = self.load()
        revenue = frame["revenue"].sum()
        customers = frame["customer_id"].nunique()
        return {
            "total_revenue": round(float(revenue), 2),
            "transactions": len(frame),
            "unique_customers": int(customers),
            "average_order_value": round(float(revenue / len(frame)), 2),
            "repeat_customer_rate": round(
                float((frame.groupby("customer_id").size() > 1).mean() * 100), 2
            ),
            "date_range": {
                "start": frame["transaction_date"].min().date().isoformat(),
                "end": frame["transaction_date"].max().date().isoformat(),
            },
        }

    def top_products(self, limit: int = 5) -> list[dict]:
        frame = self.load()
        products = (
            frame.groupby(["product_id", "product_name", "category"], as_index=False)
            .agg(revenue=("revenue", "sum"), units_sold=("quantity", "sum"), transactions=("transaction_id", "count"))
            .sort_values("revenue", ascending=False)
            .head(limit)
        )
        return [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "category": row.category,
                "revenue": round(float(row.revenue), 2),
                "units_sold": int(row.units_sold),
                "transactions": int(row.transactions),
            }
            for row in products.itertuples(index=False)
        ]

    def anomalies(self, limit: int = 10) -> list[dict]:
        frame = self.load().copy()
        features = frame[["quantity", "unit_price", "discount_pct", "revenue"]]
        model = IsolationForest(contamination=0.02, random_state=42)
        frame["anomaly"] = model.fit_predict(features)
        frame["anomaly_score"] = -model.score_samples(features)
        flagged = frame[frame["anomaly"] == -1].sort_values("anomaly_score", ascending=False).head(limit)
        return [
            {
                "transaction_id": row.transaction_id,
                "transaction_date": row.transaction_date.date().isoformat(),
                "product_name": row.product_name,
                "customer_id": row.customer_id,
                "revenue": round(float(row.revenue), 2),
                "anomaly_score": round(float(row.anomaly_score), 4),
            }
            for row in flagged.itertuples(index=False)
        ]
