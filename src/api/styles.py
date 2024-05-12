from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/style", tags=["Styles"])


@router.get("/header.css")
async def get_header_css():
    file_path = (
        Path(__file__).resolve().parent.parent / "templates" / "static" / "header.css"
    )
    return FileResponse(file_path)


@router.get("/style.css")
async def get_style_css():
    file_path = (
        Path(__file__).resolve().parent.parent / "templates" / "static" / "style.css"
    )
    return FileResponse(file_path)


@router.get("/footer.css")
async def get_footer_css():
    file_path = (
        Path(__file__).resolve().parent.parent / "templates" / "static" / "footer.css"
    )
    return FileResponse(file_path)


@router.get("/style_basket.css")
async def get_style_basket_css():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "templates"
        / "static"
        / "style_basket.css"
    )
    return FileResponse(file_path)


@router.get("/style_login.css")
async def get_style_login_css():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "templates"
        / "static"
        / "style_login.css"
    )
    return FileResponse(file_path)


@router.get("/style_reg.css")
async def get_style_reg_css():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "templates"
        / "static"
        / "style_reg.css"
    )
    return FileResponse(file_path)
