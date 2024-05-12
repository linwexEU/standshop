from pydantic import BaseModel


class SProducts(BaseModel):
    id: int
    name: str
    price: int


class SProductsAdd(BaseModel):
    name: str
    price: int
