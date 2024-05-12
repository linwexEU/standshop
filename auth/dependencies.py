import datetime
from typing import Annotated

from fastapi import Depends, Request
from jose import JWTError, jwt

from api.dependencies import users_service
from config import settings


def get_token(request: Request):
    token = request.cookies.get("auth_token")
    if not token:
        return False
    return token


async def get_current_user(
    token: Annotated[str | bool, Depends(get_token)], users_service=users_service()
):
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError:
            return False
        expire: str = payload.get("exp")
        if (not expire) or (
            int(expire) < datetime.datetime.now(datetime.UTC).timestamp()
        ):
            return False
        user_id: str = payload.get("sub")
        if not user_id:
            return False
        user = await users_service.get_one({"id": int(user_id)})
        if not user:
            return False
        return user
