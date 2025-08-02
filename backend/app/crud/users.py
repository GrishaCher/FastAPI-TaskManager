
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.core.security import auth_service
from app.db.models.users import User
from app.schemas.user import UserRegister, UserInUpdate


async def create_user(*, session: AsyncSession, user_create: UserRegister) -> User:
    db_obj = User.model_validate(
        user_create,
        update={"hashed_password": auth_service.get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(*, session: AsyncSession, db_user: User, user_in: UserInUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if not user_data:
        raise HTTPException(
                status_code=400,
                detail="поля не выбранны",
            ) 
    if "password" in user_data:
        user_data["hashed_password"] = auth_service.get_password_hash(user_data.pop("password"))
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email==email)
    curent_user = await session.scalars(statement)
    if curent_user:
        return curent_user.first()
    raise HTTPException(
                status_code=400,
                detail="данный пользователь не найден",
            ) 


async def authenticate(*, session: AsyncSession, email: str, password: str) -> User | None:
    db_user =await get_user_by_email(session=session, email=email)
    if not auth_service.verify_password(password, db_user.hashed_password):
        raise HTTPException(
                status_code=400,
                detail="неверный пароль",
            )
    return db_user
