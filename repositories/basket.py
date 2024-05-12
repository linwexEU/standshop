from sqlalchemy import delete, select, text
from sqlalchemy.orm import selectinload

from db.db import async_session_maker
from models.basket import Basket
from utils.repository import SQLAlchemyRepository


class BasketRepository(SQLAlchemyRepository):
    model = Basket

    async def get_basket_with_products(self, user_id):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .options(selectinload(self.model.products))
                .where(self.model.user_id == user_id)
            )
            result = await session.execute(query)
            return [row.convert_to_pydantic() for row in result.scalars().all()]

    async def delete_product(self, product_id, user_id):
        async with async_session_maker() as session:
            query = text(
                "DELETE FROM basket WHERE ctid IN (SELECT ctid FROM basket WHERE product_id = :product_id AND user_id = :user_id LIMIT 1)"
            )
            await session.execute(query, {"product_id": product_id, "user_id": user_id})
            await session.commit()

    async def delete_all_products(self, user_id):
        async with async_session_maker() as session:
            query = delete(self.model).where(self.model.user_id == user_id)
            await session.execute(query)
            await session.commit()
