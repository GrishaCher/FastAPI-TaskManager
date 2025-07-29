from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.sqlalchemyURL,echo=False)
async_session=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить асинхронную сессию для работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session() as session:
        yield session