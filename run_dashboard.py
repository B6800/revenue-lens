"""PyCharm-friendly launcher for the Revenue Lens Streamlit dashboard."""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    dashboard = Path(__file__).with_name("dashboard.py")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(dashboard)],
        check=False,
    )
