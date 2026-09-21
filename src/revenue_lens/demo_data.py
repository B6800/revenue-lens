from __future__ import annotations

import csv
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

PRODUCTS = [
    ("wireless-headphones", "Wireless Headphones", "Audio", 89.99),
    ("mechanical-keyboard", "Mechanical Keyboard", "Office", 119.99),
    ("smart-watch", "Smart Watch", "Wearables", 149.99),
    ("desk-lamp", "Desk Lamp", "Home Office", 44.99),
    ("usb-c-hub", "USB-C Hub", "Accessories", 39.99),
    ("everyday-hoodie", "Everyday Hoodie", "Apparel", 54.99),
]


def generate_demo_dataset(destination: Path, rows: int = 720, seed: int = 42) -> Path:
    """Create deterministic synthetic retail transactions for local demonstrations."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    randomizer = random.Random(seed)
    start = datetime.now(UTC).date() - timedelta(days=210)

    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "transaction_id",
                "transaction_date",
                "customer_id",
                "product_id",
                "product_name",
                "category",
                "quantity",
                "unit_price",
                "discount_pct",
            ],
        )
        writer.writeheader()
        for index in range(rows):
            product_id, product_name, category, unit_price = randomizer.choice(PRODUCTS)
            quantity = randomizer.choices([1, 2, 3, 4], weights=[62, 25, 10, 3])[0]
            discount = randomizer.choice([0, 0, 0, 0.05, 0.10, 0.15])
            # A few high-value transactions make anomaly detection demonstrable.
            if index in {77, 341, 618}:
                quantity, discount = 9, 0
            writer.writerow(
                {
                    "transaction_id": f"TX-{index + 1:04d}",
                    "transaction_date": (start + timedelta(days=randomizer.randrange(210))).isoformat(),
                    "customer_id": f"CUS-{randomizer.randrange(1, 151):03d}",
                    "product_id": product_id,
                    "product_name": product_name,
                    "category": category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_pct": discount,
                }
            )
    return destination
