from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import auth_service
from app.core.config import settings
from app.db.models.users import User
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_refresh_scheme = OAuth2PasswordBearer(tokenUrl="auth/refresh")
async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth_service.decode_token(token)
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise credentials_exception
    return user