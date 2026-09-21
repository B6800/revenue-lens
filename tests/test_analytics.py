from pathlib import Path

from revenue_lens.analytics import RetailAnalytics
from revenue_lens.demo_data import generate_demo_dataset


def test_overview_and_products_are_generated(tmp_path: Path) -> None:
    dataset = generate_demo_dataset(tmp_path / "transactions.csv", rows=50)
    analytics = RetailAnalytics(dataset)

    overview = analytics.overview()

    assert overview["transactions"] == 50
    assert overview["total_revenue"] > 0
    assert len(analytics.top_products()) > 0


def test_anomalies_include_explainable_transaction_fields(tmp_path: Path) -> None:
    dataset = generate_demo_dataset(tmp_path / "transactions.csv", rows=100)
    results = RetailAnalytics(dataset).anomalies()

    assert results
    assert {"transaction_id", "revenue", "anomaly_score"}.issubset(results[0])

