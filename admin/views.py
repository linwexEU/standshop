from sqladmin import ModelView

from auth.auth import get_password_hash
from models.basket import Basket
from models.products import Products
from models.users import Users

from api.dependencies import basket_service 
from services.basket import BasketService 


class UsersAdmin(ModelView, model=Users):
    column_list = [c.name for c in Users.__table__.c if c.name != "hashed_password"]
    column_details_exclude_list = [Users.hashed_password]

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    async def on_model_delete(self, model: Users, basket_service: BasketService = basket_service()) -> None:
        await basket_service.delete_all_products(user_id=Users.id)

    async def on_model_change(self, data: dict, model: Users, is_created: bool) -> None:
        data["hashed_password"] = get_password_hash(data["hashed_password"])
        

class BasketAdmin(ModelView, model=Basket):
    column_list = [c.name for c in Basket.__table__.c]

    name = "Корзина"
    name_plural = "Корзина"
    icon = "fa-solid fa-trash"


class ProductsAdmin(ModelView, model=Products):
    column_list = [c.name for c in Products.__table__.c]

    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-cart-shopping"
