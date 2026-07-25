from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'DEFAULT_SECRET_KEY'
    yandex_disk_token: Optional[str] = None
    report_format: str = '%d.%m.%Y'

    class Config:
        env_file = '.env'
        env_prefix = 'APP_'


settings = Settings()
