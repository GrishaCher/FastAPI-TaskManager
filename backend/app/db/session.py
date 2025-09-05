from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.sqlalchemyURL,echo=False,
    pool_recycle=300,  # Пересоздавать соединения каждые 300 сек
    pool_pre_ping=True,  # Проверять соединение перед использованием
    pool_timeout=30,  # Ждать свободного соединения до 30 сек
    )
async_session=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить асинхронную сессию для работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session() as session:
        yield session