from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import auth_service
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import get_user_by_email
from app.schemas.users import UserResponse

import logging

logger = logging.getLogger("app")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"попытка авторизации пользователя с токеном {token}")
    try:
        payload = auth_service.decode_token(token)
        logger.debug(f"нагрузка токена: {payload}")
        if payload is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    get_email = payload["sub"]
    logger.info(f"email пользователя {get_email}")
    if get_email is None:
        raise credentials_exception
    user = await get_user_by_email(session=db, email=get_email)
    logger.info(f"получен пользователь {user}")
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь неактивен")
    return user


async def check_refresh(token: str = Header(..., alias="X-Token")) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_service.verify_refresh_token(token)
    except JWTError:
        raise credentials_exception
    return payload
