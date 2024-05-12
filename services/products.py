from schemas.products import SProductsAdd
from utils.repository import AbstractRepository


class ProductsService:
    def __init__(self, product_repo: AbstractRepository):
        self.product_repo = product_repo()

    async def get_all(self, filters: dict | None = None):
        result = await self.product_repo.get_all(filters)
        return result

    async def insert_data(self, params: SProductsAdd):
        product_data = params.model_dump()
        await self.product_repo.insert_data(product_data)
