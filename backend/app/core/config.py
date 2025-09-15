from pydantic_settings import BaseSettings
from pydantic import computed_field
class Settings(BaseSettings):
    #Настройки авторизации 
    SECRET_KEY: str 
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    #Настройки базы данных
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str

    #Настройки отладки
    DEBUG: bool = False
    LOG_LEVEL:str="DEBUG"
    LOG_FILE:str=""
    CONSOLE_LOG:bool=False

    # SMTP настройки
    SMTP_HOST: str 
    SMTP_PORT: int 
    SMTP_USER: str
    SMTP_PASSWORD: str
    smtp_use_tls:bool
    
    # Frontend URL для ссылок
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Время жизни verification токена
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    @computed_field
    @property
    def sqlalchemyURL(self)->str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    class Config:
        env_file = ".env"

settings = Settings()  