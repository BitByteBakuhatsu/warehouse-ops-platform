import pytest

from warehouse.io import load_products
from warehouse.models import Product


def test_load_products_returns_valid_products(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "sku,name,category,price\n"
        "HEA005,Sony Headphones,Audio,149.99\n"
        "MOU002,Wireless Mouse,Accessories,24.99\n"
    )

    products = load_products(csv_file)

    assert len(products) == 2
    assert isinstance(products[0], Product)
    assert products[0].sku == "HEA005"


def test_load_products_skips_empty_sku(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "sku,name,category,price\n"
        "HEA005,Sony Headphones,Audio,149.99\n"
        ",Invalid Product,Accessories,50.00\n"
        "MOU002,Wireless Mouse,Accessories,24.99\n"
    )

    products = load_products(csv_file)

    assert len(products) == 2
    assert products[0].sku == "HEA005"
    assert products[1].sku == "MOU002"


def test_load_products_skips_non_numeric_price(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "sku,name,category,price\n"
        "HEA005,Sony Headphones,Audio,149.99\n"
        "KOU001,Wireless Keyboard,Accessories,abc\n"
        "MOU002,Wireless Mouse,Accessories,24.99\n"
    )

    products = load_products(csv_file)

    assert len(products) == 2
    assert products[0].sku == "HEA005"
    assert products[1].sku == "MOU002"


def test_load_products_raises_key_error_for_invalid_header(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "SKU,name,category,price\nHEA005,Sony Headphones,Audio,149.99\n"
    )

    with pytest.raises(KeyError):
        load_products(csv_file)
