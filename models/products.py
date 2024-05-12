from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class Products(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    basket = relationship("Basket", back_populates="products")

    def __str__(self):
        return f"{self.name}"
