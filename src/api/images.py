import io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/img", tags=["Images"])


@router.get("/back/")
async def get_back_image():
    with open("templates/static/back.jpg", "rb") as file:
        image = file.read()
        return StreamingResponse(io.BytesIO(image), media_type="image/jpg")


@router.get("/basket/")
async def get_basket_image():
    with open("templates/static/basket.png", "rb") as file:
        image = file.read()
        return StreamingResponse(io.BytesIO(image), media_type="image/png")


@router.get("/gold/")
async def get_gold_image():
    with open("templates/static/gold.png", "rb") as file:
        image = file.read()
        return StreamingResponse(io.BytesIO(image), media_type="image/jpg")
