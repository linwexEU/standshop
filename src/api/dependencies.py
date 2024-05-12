from repositories.basket import BasketRepository
from repositories.products import ProductsRepository
from repositories.users import UsersRepository
from services.basket import BasketService
from services.products import ProductsService
from services.users import UsersService


def users_service():
    return UsersService(UsersRepository)


def products_service():
    return ProductsService(ProductsRepository)


def basket_service():
    return BasketService(BasketRepository)
