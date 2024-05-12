from fastapi_cache.decorator import cache

from schemas.basket import SBasket
from utils.repository import AbstractRepository


class BasketService:
    def __init__(self, basket_repo: AbstractRepository):
        self.basket_repo = basket_repo()

    async def get_all(self, filters: dict | None = None):
        result = await self.basket_repo.get_all(filters)
        return result

    async def insert_data(self, params: SBasket):
        basket_params = params.model_dump()
        await self.basket_repo.insert_data(basket_params)

    @cache(expire=20)
    async def get_basket_with_products(self, user_id):
        dct = {}
        result_from_db = await self.basket_repo.get_basket_with_products(user_id)

        for item in result_from_db:
            if item.products.name not in dct.keys():
                dct[item.products.name] = {}
                dct[item.products.name]["id"] = item.products.id
                dct[item.products.name]["count"] = 1
                dct[item.products.name]["price"] = item.products.price
            else:
                dct[item.products.name]["count"] += 1
            dct[item.products.name]["total_price"] = (
                dct[item.products.name]["count"] * dct[item.products.name]["price"]
            )

        return dct

    async def delete_product(self, product_id, user_id):
        await self.basket_repo.delete_product(product_id, user_id)

    async def delete_all_products(self, user_id):
        await self.basket_repo.delete_all_products(user_id)
