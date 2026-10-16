import argparse
import logging
from pathlib import Path

from warehouse.io import load_products

logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Load products from a CSV file")
    parser.add_argument("--file", required=True, type=Path, help="Path to csv file")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if not args.file.exists():
        logger.error("File does not exist: %s", args.file)
        return 1
    if not args.file.is_file():
        logger.error("Path is not a file: %s", args.file)
        return 1

    products = load_products(args.file)

    print(f"Loaded {len(products)} valid products from {args.file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
