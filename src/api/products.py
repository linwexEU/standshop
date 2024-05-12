from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import products_service
from auth.dependencies import get_current_user
from config import settings
from models.users import Users
from schemas.products import SProducts, SProductsAdd
from services.products import ProductsService

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/")
async def get_product(
    products_service: Annotated[ProductsService, Depends(products_service)]
) -> list[SProducts]:
    result = await products_service.get_all()
    return result


@router.post("/add/")
async def add_product(
    params: SProductsAdd,
    products_service: Annotated[ProductsService, Depends(products_service)],
    user: Annotated[Users, Depends(get_current_user)],
):
    if not user or user.email != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await products_service.insert_data(params)
    return {"message": "Done!"}
