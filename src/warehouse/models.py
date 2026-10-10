from dataclasses import dataclass
from decimal import Decimal


class InvalidProductError(ValueError):
    """Raised when a Product fails validation."""


@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: Decimal

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise InvalidProductError(
                f"SKU cannot be empty, got sku={self.sku!r} name={self.name!r}"
            )
        if not self.category.strip():
            raise InvalidProductError(
                f"Category cannot be empty, got category={self.category!r} name={self.name!r} sku={self.sku!r}"
            )
        if not self.name.strip():
            raise InvalidProductError(
                f"Name cannot be empty, got {self.name!r} sku={self.sku!r}"
            )
        if (
            self.price < 0
        ):  # Price 0 is valid: marketing items and giveaways are recorded at zero cost.
            raise InvalidProductError(
                f"Price must be >= 0, got {self.price!r} sku={self.sku!r} name={self.name!r}"
            )
