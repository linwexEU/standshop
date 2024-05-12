import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    ADMIN_EMAIL: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    class ConfigDict:
        env_file = dotenv_path


settings = Settings()
