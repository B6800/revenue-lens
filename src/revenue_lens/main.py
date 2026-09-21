import os
import tempfile
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .analytics import RetailAnalytics
from .web import DASHBOARD_HTML

app = FastAPI(
    title="Revenue Lens API",
    version="0.1.0",
    description="Retail intelligence endpoints for revenue, product performance, and anomaly detection.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@lru_cache
def analytics() -> RetailAnalytics:
    if os.getenv("VERCEL"):
        return RetailAnalytics(Path(tempfile.gettempdir()) / "revenue_lens" / "demo_transactions.csv")
    root = Path(__file__).resolve().parents[2]
    return RetailAnalytics(root / "data" / "demo_transactions.csv")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)


@app.get("/analytics/overview")
def get_overview() -> dict:
    return analytics().overview()


@app.get("/analytics/products")
def get_top_products(limit: int = Query(default=5, ge=1, le=20)) -> list[dict]:
    return analytics().top_products(limit)


@app.get("/analytics/anomalies")
def get_anomalies(limit: int = Query(default=10, ge=1, le=50)) -> list[dict]:
    return analytics().anomalies(limit)
