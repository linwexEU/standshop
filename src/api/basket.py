from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from api.dependencies import basket_service
from auth.dependencies import get_current_user
from models.users import Users
from schemas.basket import SBasket
from services.basket import BasketService
from utils.message import flash

router = APIRouter(prefix="/basket", tags=["Basket"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def render_basket(
    request: Request,
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Annotated[Users, Depends(get_current_user)],
):
    try:
        products = await basket_service.get_basket_with_products(user_id=user.id)
        full_price = sum(
            [value["count"] * value["price"] for value in products.values()]
        )
        return templates.TemplateResponse(
            "basket.html",
            {"request": request, "products": products, "full_price": full_price},
        )
    except:
        flash(request=request, message="Войдите или зарегистрируйтесь")
        return RedirectResponse(
            "/#message", status_code=status.HTTP_303_SEE_OTHER
        )


@router.post("/add/{product_id}/")
async def add_to_basket(
    request: Request,
    response: Response,
    product_id: int,
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Annotated[Users, Depends(get_current_user)],
):
    try:
        basket_model = SBasket(product_id=product_id, user_id=user.id)
        await basket_service.insert_data(basket_model)

        response.status_code = status.HTTP_303_SEE_OTHER
        response.headers["Location"] = "/#main"
        return response
    except:
        flash(request=request, message="Войдите или зарегистрируйтесь")
        return RedirectResponse(
            "/#message", status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/get_products/")
async def render_get_products(
    request: Request,
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Annotated[Users, Depends(get_current_user)],
) -> dict:
    try:
        result = await basket_service.get_basket_with_products(user_id=user.id)
        return result
    except:
        flash(request=request, message="Войдите или зарегистрируйтесь")
        return RedirectResponse(
            "/#message", status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/delete/{product_id}/")
async def render_delete_product(
    request: Request,
    product_id: int,
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Annotated[Users, Depends(get_current_user)],
):
    try:
        await basket_service.delete_product(product_id, user.id)
        return RedirectResponse("/basket/", status_code=status.HTTP_303_SEE_OTHER)
    except:
        flash(request=request, message="Войдите или зарегистрируйтесь")
        return RedirectResponse(
            "/#message", status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/delete_all_products/")
async def render_delete_all_products(
    request: Request,
    basket_service: Annotated[BasketService, Depends(basket_service)],
    user: Annotated[Users, Depends(get_current_user)],
):
    try:
        await basket_service.delete_all_products(user_id=user.id)
        return RedirectResponse("/basket/", status_code=status.HTTP_303_SEE_OTHER)
    except:
        flash(request=request, message="Войдите или зарегистрируйтесь")
        return RedirectResponse(
            "/#message", status_code=status.HTTP_303_SEE_OTHER
        )
