from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    db_user: str = "retrieve"
    db_password: str
    db_domain: str
    db_port: int = 5432
    db_name: str = "retrieve_app"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_domain}:{self.db_port}/{self.db_name}"

    model_config = {
        "env_file": Path(__file__).resolve().parents[2] / ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


settings = Settings()
