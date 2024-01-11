import os

from pydantic_settings import BaseSettings, SettingsConfigDict


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_file_path = os.path.join(root_dir, ".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=env_file_path)


settings = Settings()
