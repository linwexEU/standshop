from pydantic import BaseModel

from schemas.products import SProducts


class SBasket(BaseModel):
    product_id: int
    user_id: int


class SBasketWithProducts(BaseModel):
    id: int
    product_id: int
    user_id: int
    products: SProducts
