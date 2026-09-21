"""PyCharm-friendly launcher for the Revenue Lens FastAPI service."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "revenue_lens.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
