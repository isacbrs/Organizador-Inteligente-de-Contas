from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    NEBIUS_API_KEY: str = "" # Vazio por enquanto até a Fase 2

    class Config:
        env_file = ".env"

settings = Settings()