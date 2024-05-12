from typing import Annotated

from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
                     Response, status)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from api.dependencies import users_service
from auth.auth import (authenticate_user, create_access_token,
                           get_password_hash)
from schemas.users import SUsers
from services.users import UsersService
from utils.message import flash, get_flash_message

router = APIRouter(prefix="/auth", tags=["Users"])
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flash_message"] = get_flash_message


@router.get("/register/")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/")
async def register_user(
    request: Request,
    response: Response,
    username: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    user = await users_service.get_one({"email": email})
    if user:
        flash(request=request, message="Email занят")
        return RedirectResponse(
            "/auth/register/", status_code=status.HTTP_303_SEE_OTHER
        )

    hashed_password = get_password_hash(password)
    user_model = SUsers(username=username, email=email, hashed_password=hashed_password)

    await users_service.insert_data(user_model)

    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = "/auth/login/"
    return response


@router.get("/login/")
async def login_page(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@router.post("/login/")
async def login_user(
    request: Request,
    response: Response,
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
):
    try:
        user = await authenticate_user(email, password)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("auth_token", access_token, httponly=True)

        response.status_code = status.HTTP_303_SEE_OTHER
        response.headers["Location"] = "/"

        return response
    except:
        flash(request=request, message="Неверный пароль / email")
        return RedirectResponse("/auth/login/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("auth_token")
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = "/"
    return response
