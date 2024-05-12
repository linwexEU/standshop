from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from admin.auth import authentication_backend
from admin.views import BasketAdmin, ProductsAdmin, UsersAdmin
from api.dependencies import basket_service, products_service
from api.routers import all_routers
from auth.dependencies import get_current_user
from config import settings
from db.db import engine
from models.users import Users
from services.basket import BasketService
from services.products import ProductsService
from utils.message import get_flash_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="redis-cache")
    yield


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)

templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flash_message"] = get_flash_message

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BasketAdmin)
admin.add_view(ProductsAdmin)


@app.get("/")
async def render_main(
    request: Request,
    products_service: Annotated[ProductsService, Depends(products_service)],
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Users = Depends(get_current_user),
):
    @cache(expire=60)
    async def get_all_products():
        return await products_service.get_all()

    try:
        products_from_basket = await basket_service.get_basket_with_products(
            user_id=user.id
        )
        product_count = sum(
            [value["count"] for _, value in products_from_basket.items()]
        )
    except:
        product_count = 0
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "user": user,
            "products": await get_all_products(),
            "product_count": product_count,
        },
    )
