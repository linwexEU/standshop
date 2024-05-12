from models.products import Products
from utils.repository import SQLAlchemyRepository


class ProductsRepository(SQLAlchemyRepository):
    model = Products
