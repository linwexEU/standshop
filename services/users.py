from schemas.users import SUsers
from utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo = users_repo()

    async def get_all(self, filters: dict | None = None):
        result = await self.users_repo.get_all(filters)
        return result

    async def get_one(self, filters: dict | None = None):
        result = await self.users_repo.get_one(filters)
        return result

    async def insert_data(self, params: SUsers):
        user_params = params.model_dump()
        await self.users_repo.insert_data(user_params)
