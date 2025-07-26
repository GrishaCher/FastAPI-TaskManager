from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn = "postgresql+asyncpg://user:pass@localhost:5432/db"
    DEBUG: bool = False
    SECRET_KEY: str 
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()  