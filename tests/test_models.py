from decimal import Decimal

import pytest

from warehouse.models import InvalidProductError, Product


def test_valid_product_keeps_values():
    product = Product(
        sku="LAP002",
        name="Logitech keyboard",
        category="Accessories",
        price=Decimal("100.00"),
    )

    assert product.sku == "LAP002"
    assert product.name == "Logitech keyboard"
    assert product.category == "Accessories"
    assert product.price == Decimal("100.00")


def test_zero_price_is_valid():
    product = Product(
        sku="LAP002",
        name="Logitech keyboard",
        category="Accessories",
        price=Decimal(0),
    )

    assert product.price == Decimal(0)


def test_empty_sku_raises_invalid_product_error():
    with pytest.raises(InvalidProductError):
        Product(
            sku="",
            name="Logitech keyboard",
            category="Accessories",
            price=Decimal("100.00"),
        )


def test_whitespace_sku_raises_invalid_product_error():
    with pytest.raises(InvalidProductError):
        Product(
            sku=" ",
            name="Logitech keyboard",
            category="Accessories",
            price=Decimal("100.00"),
        )


def test_negative_price_raises_invalid_product_error():
    with pytest.raises(InvalidProductError):
        Product(
            sku="LAP002",
            name="Logitech keyboard",
            category="Accessories",
            price=Decimal("-100.00"),
        )
