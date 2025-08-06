from fastapi import Depends, HTTPException, status,Header
from jose import JWTError
from app.core.security import auth_service
from app.db.models import User
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_current_user(db: AsyncSession = Depends(get_session), token: str =Header(...,alias="Authorization"))->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_service.decode_token(token)
    except JWTError as e:
        raise credentials_exception
    get_email=payload["sub"]
    if get_email is None:
        raise credentials_exception
    user = await db.scalar(select(User).where(User.email == get_email)).first()
    if user is None:
        raise credentials_exception
    return user
async def check_refresh(token: str =Header(...,alias="X-Token"))->str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=auth_service.verify_refresh_token(token)
    except JWTError as e:
        # здесь можно логировать данные о самой ошибке через e
        raise credentials_exception
    return payload