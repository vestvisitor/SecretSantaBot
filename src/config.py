from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from typing import Dict, List


class Settings(BaseSettings):

    DB_NAME: str

    BOT_TOKEN: str

    GROUP_ID: int

    RESTRICTED_NUMBERS: List[int]

    PARTICIPANTS: Dict[str, int]

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"sqlite:///src/database/{self.DB_NAME}.db"

    model_config = SettingsConfigDict(
        env_file="src/.env"
    )


settings = Settings()
