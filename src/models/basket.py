from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from schemas.basket import SBasketWithProducts
from schemas.products import SProducts


class Basket(Base):
    __tablename__ = "basket"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    products = relationship("Products", back_populates="basket")
    users = relationship("Users", back_populates="basket")

    def convert_to_pydantic(self):
        return SBasketWithProducts(
            id=self.id,
            product_id=self.product_id,
            user_id=self.user_id,
            products=SProducts(
                id=self.products.id, name=self.products.name, price=self.products.price
            ),
        )

    def __str__(self):
        return f"Basket({self.id})"
