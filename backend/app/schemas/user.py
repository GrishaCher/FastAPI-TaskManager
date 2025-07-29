from app.schemas.base import BaseModelWithConfig
from datetime import datetime
from typing import Optional
from pydantic import EmailStr #, HttpUrl 

class UserLogin(BaseModelWithConfig):
    email: str
    password: str
class UserRegister(UserLogin):
    username:str

class UserInUpdate(UserRegister):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    created_at: Optional[datetime]= None
    #image: Optional[HttpUrl] = None   Для фото профиля
class UserWithToken(UserRegister):
    token:str
class UserResponse(BaseModelWithConfig):
    user: UserWithToken
    