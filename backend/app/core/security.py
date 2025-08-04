from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings



class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire_days = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    def get_password_hash(self, password: str) -> str:
        hashed = self.pwd_context.hash(password)
        return hashed

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        valid = self.pwd_context.verify(plain_password, hashed_password)
        return valid

    def create_access_token(self, user_email: str) -> str:
        expire = datetime.now(timezone.utc) + self.access_token_expire_minutes
        to_encode = {"sub": str(user_email), "exp": expire}
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def create_refresh_token(self, user_email: str) -> str:
        expire = datetime.now(timezone.utc) + self.refresh_token_expire_days
        to_encode = {"sub": str(user_email), "exp": expire}
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token


    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            return None
    def verify_refresh_token(self, token: str) -> str:
        payload = self.decode_token(token)
        if not payload:
            raise JWTError("Некорректный токен")
        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise JWTError("Истёк срок токена")
        
        return payload["sub"]


auth_service = AuthService()
