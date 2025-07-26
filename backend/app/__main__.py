from app.core.config import settings
from app.core.session import get_db_sessionmaker
from fastapi import FastAPI
print(settings.POSTGRES_URL)
LocalSession=get_db_sessionmaker(postgres_url=settings.POSTGRES_URL)
#app=FastAPI()