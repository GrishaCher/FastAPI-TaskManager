from pydantic_settings import BaseSettings
from pydantic import computed_field
class Settings(BaseSettings):
    #POSTGRES_URL: str 
    DEBUG: bool = False
    SECRET_KEY: str 
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    @computed_field
    @property
    def sqlalchemyURL(self)->str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    class Config:
        env_file = ".env"

settings = Settings()  