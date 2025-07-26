from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

def get_db_sessionmaker(postgres_url: str):
    engine = create_async_engine(postgres_url,echo=False)
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )