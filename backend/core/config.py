from pathlib import Path

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str = ""

    @field_validator("jwt_secret")
    @classmethod
    def is_valid_secret(cls, value: str):
        if not value:
            raise ValueError("JWT Secret must be defined in the .env file")
        elif len(value) < 32:
            print("Please consider using a stronger secret for the JWT Secret")

        return value

    jwt_access_token_expiration_minutes: int = 15
    jwt_secret_token_expiration_minutes: int = 60

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
        "extra": "ignore",
    }


settings = Settings()
