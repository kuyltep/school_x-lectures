from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class Configs(BaseSettings):
    openai_base_url: HttpUrl
    openai_api_key: str
    openai_model: str

    model_config = SettingsConfigDict(env_file=".env")


# configs = Configs()
