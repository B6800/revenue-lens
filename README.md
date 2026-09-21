# Revenue Lens

**Revenue Lens** is a portfolio-ready retail-intelligence platform that turns transaction data into decisions. It exposes a documented FastAPI service and a Streamlit dashboard for revenue performance, customer behaviour, product performance, and anomalous-transaction review.

The project is designed to demonstrate practical Python engineering rather than a standalone notebook: modular application code, data validation, reproducible demo data, API testing, containerisation, and an explainable machine-learning workflow.

## What it demonstrates

- **Data engineering:** validates and transforms transaction data into analysis-ready revenue metrics.
- **Business analytics:** calculates revenue, average order value, repeat-customer rate, and product performance.
- **Machine learning:** applies Isolation Forest to flag unusual transactions for human review.
- **Backend development:** offers typed, documented REST endpoints through FastAPI.
- **Data product UX:** provides a Streamlit dashboard for non-technical stakeholders.
- **Software quality:** includes unit and API tests, a reproducible data generator, and Docker support.

## Architecture

```text
Synthetic CSV data → pandas validation & transformation → analytics service
                                                      ├─ FastAPI REST API /docs
                                                      └─ Streamlit dashboard
                                                           └─ anomaly review queue
```

## Features

| Area | Capability |
| --- | --- |
| Revenue | Total revenue, transactions, average order value, and reporting date range |
| Customers | Unique-customer count and repeat-customer rate |
| Products | Revenue-ranked product performance with unit and transaction counts |
| Risk review | Isolation Forest flags statistically unusual transactions |
| API | Interactive OpenAPI documentation at `/docs` |
| Dashboard | Executive metrics, product chart, and anomaly queue |

## Quick start

Requires Python 3.11+.

```bash
git clone <your-repository-url>
cd revenue-lens
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dashboard,dev]"
uvicorn revenue_lens.main:app --reload
```

The API creates a deterministic synthetic dataset automatically on its first run. Open:

- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

In a second terminal, start the dashboard:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run dashboard.py
```

Then open [http://localhost:8501](http://localhost:8501).

## API endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Service health check |
| `GET /analytics/overview` | Executive revenue and customer metrics |
| `GET /analytics/products?limit=5` | Top products by revenue |
| `GET /analytics/anomalies?limit=10` | Transactions flagged for review |

## Run checks

```powershell
pytest
ruff check .
```

## Run with Docker

```bash
docker compose up --build
```

## Data and responsible-use note

The included data is entirely synthetic and exists only for demonstration. An anomaly score is a prioritisation signal, not proof of fraud; a person should review flagged transactions before any business decision is made.

## Next steps

- Replace the demo CSV with a versioned public dataset or a database connector.
- Add monthly forecasting and model evaluation metrics.
- Add authentication and role-based access for production use.
- Deploy the API and dashboard, then link both from a portfolio case study.
