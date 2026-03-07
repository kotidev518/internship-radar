import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "Internship Radar API"
    database_url: str = "postgresql+psycopg2://user:password@localhost/internship_radar"
    gemini_api_key: str = ""
    scraper_interval: int = 12 # hours
    batch_size: int = 20
    frontend_url: str = "http://localhost:3000"
    environment: str = "dev" # dev or production

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, '.env'),
        extra='ignore'
    )

settings = Settings()
