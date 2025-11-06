from app.schemas.base import BaseModelWithConfig
from datetime import datetime


class TokenBase(BaseModelWithConfig):
    access_token: str
    token_type: str = "bearer"


class Token(TokenBase):
    refresh_token: str


class TokenPayload(BaseModelWithConfig):
    sub: str | None = None
    exp: datetime | None = None
