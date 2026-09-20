from pathlib import Path

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Retrieve"
    app_debug: bool = False
    app_demo: bool = False

    app_address: str = "localhost:8001"

    storage_secret: str = ""

    @field_validator("storage_secret")
    @classmethod
    def is_valid_secret(cls, value: str):
        if not value:
            raise ValueError("Storage secret must be defined in the .env file")
        elif len(value) < 32:
            print("Please consider using a stronger storage secret")

        return value

    timeout_time_httpx_seconds: int = 60

    model_config = {
        "env_file": Path(__file__).resolve().parents[2] / ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()
