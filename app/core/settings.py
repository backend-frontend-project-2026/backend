from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    DB_SCHEME: str = 'postgresql+asyncpg'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 2_592_000
    REFRESH_COOKIE_NAME: str = 'refresh_token'
    JWT_ALGORITHM: str = 'HS256'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def DATABASE_URL(self) -> str:
        return URL.create(
            drivername=self.DB_SCHEME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)

    @property
    def ALEMBIC_DATABASE_URL(self) -> str:
        return URL.create(
            drivername='postgresql+psycopg',
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)


settings = Settings()
