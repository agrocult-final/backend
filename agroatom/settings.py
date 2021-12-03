from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings, Field
from yarl import URL

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    environment: str = "develop"
    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "agroatom"
    db_pass: str = "agroatom"
    db_base: str = "agroatom"
    db_echo: bool = False

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    s3_url: str = Field(...)
    s3_access_key: str = Field(...)
    s3_secret_key: str = Field(...)
    s3_url_expire: int = Field(default=8200)
    s3_bucket_name: str = Field(default="agroatom")

    model_path: str = "./agroatom/cv/model/best.pt"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    class Config:
        env_file = ".env"
        env_prefix = "AGROATOM_"
        env_file_encoding = "utf-8"


settings = Settings()
