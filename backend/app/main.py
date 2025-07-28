from app.core.config import settings
from app.core.session import get_db_sessionmaker
from fastapi import FastAPI
print(settings.sqlalchemyURL)
LocalSession=get_db_sessionmaker(postgres_url=settings.sqlalchemyURL)
#app=FastAPI()