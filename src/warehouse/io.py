import csv
import logging
from decimal import Decimal, InvalidOperation
from pathlib import Path

from warehouse.models import InvalidProductError, Product

logger = logging.getLogger(__name__)


def load_products(path: Path) -> list[Product]:
    products: list[Product] = []
    rejected = 0
    with path.open(newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                product = Product(
                    sku=row["sku"],
                    name=row["name"],
                    category=row["category"],
                    price=Decimal(row["price"]),
                )
            except InvalidProductError as exc:
                logger.warning("Row %s rejected: %r", line_no, exc)
                rejected += 1
                continue
            except InvalidOperation:
                logger.warning(
                    "Row %s rejected: invalid price %r for product "
                    "SKU: %r, Name: %r. Expected a valid decimal number.",
                    line_no,
                    row.get("price"),
                    row.get("sku"),
                    row.get("name"),
                )
                rejected += 1
                continue
            products.append(product)
    loaded_rows = len(products)
    logger.info("%s rows were rejected and %s were loaded", rejected, loaded_rows)
    return products
