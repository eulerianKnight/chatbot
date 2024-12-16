import os
from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from services.secret_manager import get_secret_by_arn
from functools import lru_cache

load_dotenv()
    
DB_SECRETS = get_secret_by_arn(secret_arn=os.getenv("AWS_SECRET_ARN_DB"))
API_SECRETS = get_secret_by_arn(secret_arn=os.getenv("AWS_SECRET_ARN_APIS"))

class Settings(BaseSettings):
    DB_NAME: str = DB_SECRETS.get("dbInstanceIdentifier")
    DB_USERNAME: str = DB_SECRETS.get("username")
    DB_PASSWORD: str = DB_SECRETS.get("password")
    DB_ENDPOINT: str = DB_SECRETS.get("host")
    DB_PORT: int = DB_SECRETS.get("port")
    SECRET_KEY: str = API_SECRETS.get("AUTH_SECRET_KEY")
    OPENAI_API_KEY: str = API_SECRETS.get("OPENAI_API_KEY")
    TAVILY_SEARCH_API_KEY: str = API_SECRETS.get("TAVILY_SEARCH_API_KEY")

@lru_cache
def get_settings() -> Settings:
    return Settings()