from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.core.security import auth_service
from app.db.models import User
from app.schemas.users import UserRegister, UserInUpdate

import logging
logger = logging.getLogger("app")

async def create_user(*, session: AsyncSession, user_create: UserRegister) -> User:
    db_obj = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password= auth_service.get_password_hash(user_create.password)
    )
    logger.debug(f"попытка сохранить пользователя с email: {db_obj.email}")
    
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    logger.info(f"пользователь с email: {db_obj.email} сохранён")
    return db_obj


async def update_user(*, session: AsyncSession, db_user: User, user_in: UserInUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if not user_data:
        logger.debug("нет данных обновления")
        raise HTTPException(
                status_code=400,
                detail="поля не выбранны",
            ) 
    if "password" in user_data:
        user_data["hashed_password"] = auth_service.get_password_hash(user_data.pop("password"))
    for key, value in user_data.items():
        setattr(db_user, key, value)
    logger.info(f"пользователь обновлён с email: {db_user.email}")
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    logger.info(f"пользователь с email: {db_user.email} сохранён")
    return db_user


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement =await session.execute(select(User).where(User.email==email))
    current_user = statement.scalars().first()
    return current_user
async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    statement = await session.execute(select(User).where(User.username == username))
    current_user = statement.scalars().first()
    return current_user

async def get_user_by_id(*, session: AsyncSession, id: int) -> User | None:
    current_user = await session.get(User, id)
    return current_user
async def authenticate(*, session: AsyncSession, email: str, password: str) -> User | None:
    db_user =await get_user_by_email(session=session, email=email)
    if not auth_service.verify_password(password, db_user.hashed_password):
        raise HTTPException(
                status_code=401,
                detail="неверный пароль",
            )
    return db_user
