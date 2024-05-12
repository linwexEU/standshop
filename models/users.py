from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class Users(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    basket = relationship("Basket", back_populates="users")

    def __str__(self):
        return f"{self.username}"
