from pydantic import SecretStr, HttpUrl
from pydantic_settings import SettingsConfigDict, BaseSettings

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

class OpenAISettings(BaseSettings):
  
  openai_api_key: SecretStr
  openai_base_url: HttpUrl
  
  model_config = SettingsConfigDict(env_file=".env")
  
if __name__ == "__main__":
  configs = OpenAISettings()