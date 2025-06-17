from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_PUBLISHABLE_KEY: str = os.getenv("SUPABASE_PUBLISHABLE_KEY")
    SUPABASE_SECRET_KEY: str = os.getenv("SUPABASE_SECRET_KEY") # This is crucial for server-side
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL")

    SANITY_PROJECT_ID: str = os.getenv("SANITY_PROJECT_ID")
    SANITY_DATASET: str = os.getenv("SANITY_DATASET", "production")
    SANITY_API_TOKEN: str = os.getenv("SANITY_API_TOKEN")

settings = Settings()

