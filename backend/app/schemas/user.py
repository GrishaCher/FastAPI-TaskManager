from app.schemas.base import BaseModelWithConfig
from app.schemas.token import Token
from datetime import datetime
from typing import Optional
from pydantic import EmailStr #, HttpUrl 

class UserLogin(BaseModelWithConfig):
    email: EmailStr
    password: str
class UserRegister(UserLogin):
    username:str
class UserResponse(BaseModelWithConfig):
    email:EmailStr
    username: str
class UserWithTime(UserResponse):
    created_at:datetime=None
    update_at:datetime=None

class UserInUpdate(UserRegister):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None 
    created_at: Optional[datetime]= None
    #image: Optional[HttpUrl] = None   Для фото профиля
class UserWithToken(UserResponse):
    token:Token

# class UserWithTokenResponse(BaseModelWithConfig):
#     user: UserWithToken
    