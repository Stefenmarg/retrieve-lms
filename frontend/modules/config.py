from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Retrieve"
    app_debug: bool = False
    app_address: str = "localhost:8001"

    model_config = {
        "env_file": Path(__file__).resolve().parents[2] / ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()
