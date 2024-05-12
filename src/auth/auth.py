import datetime

from jose import jwt
from passlib.context import CryptContext

from api.dependencies import users_service
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str, users_service=users_service()):
    user = await users_service.get_one({"email": email})

    if not user:
        return False

    if not (user and verify_password(password, user.hashed_password)):
        return False

    return user
