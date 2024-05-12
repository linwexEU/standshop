from pydantic import BaseModel, EmailStr


class SUsers(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class SUsersResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
