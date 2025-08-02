from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import auth_service
from app.db.models.users import User
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_refresh_scheme = OAuth2PasswordBearer(tokenUrl="auth/refresh")
async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme))->User:
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