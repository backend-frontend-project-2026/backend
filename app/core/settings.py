from datetime import timedelta

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
    ACCESS_TOKEN_EXPIRE_SECONDS: int = int(timedelta(minutes=15).total_seconds())
    REFRESH_TOKEN_EXPIRE_SECONDS: int = int(timedelta(minutes=30).total_seconds())
    REFRESH_COOKIE_NAME: str = 'refresh_token'
    JWT_ALGORITHM: str = 'HS256'

    RBAC_ADMIN_ROLE: str = 'admin'
    RBAC_PUBLIC_ROLE: str = 'public'
    RBAC_ADMIN_EMAIL: str = 'admin@admin.com'
    RBAC_ADMIN_PASSWORD: str = 'adminpassword'
    RBAC_ADMIN_FIRST_NAME: str = 'Admin'
    RBAC_ADMIN_LAST_NAME: str = 'User'

    LOG_LEVEL: str = 'INFO'
    LOG_FILE_PATH: str = 'logs/app.log'

    SMTP_HOST: str = 'smtp.yandex.ru'
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ''
    SMTP_PASSWORD: str = ''
    SMTP_FROM_EMAIL: str = ''
    SMTP_FROM_NAME: str = 'Roomie Match'
    SMTP_STARTTLS: bool = True
    SMTP_SSL_TLS: bool = False

    EMAIL_NOTIFICATIONS_ENABLED: bool = True
    EMAIL_CONFIRMATION_CODE_EXPIRE_MINUTES: int = 15
    PASSWORD_RESET_CODE_EXPIRE_MINUTES: int = 15

    FRONTEND_BASE_URL: str = 'http://localhost:3000'

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