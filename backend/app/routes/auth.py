from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError

from app.schemas.users import UserRegister, UserLogin, UserResponse,UserWithToken
from app.schemas.tokens import Token
from app.core.security import auth_service
from app.core.deps import check_refresh
from app.db.session import get_session
from app.crud.users import get_user_by_email, create_user, authenticate, get_user_by_username

from sqlalchemy.ext.asyncio import AsyncSession

import logging
logger = logging.getLogger("app")

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserWithToken)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_session))-> UserWithToken:
    logger.debug("защёл в роут регистрации")
    
    if await get_user_by_email(session=db,email=user_data.email):
        raise HTTPException(status_code=401,
                             detail="Пользователь с таким email уже существует") 
    
    logger.debug(f"пользователя с таким email {user_data.email} пока нет")
    if await get_user_by_username(session=db,username=user_data.username):
        raise HTTPException(status_code=401,
                             detail="Пользователь с таким именем уже существует") 
    logger.debug(f"пользователя с таким username {user_data.username} пока нет")
    try:
        new_user=await create_user(session=db,user_create=user_data)
        logger.info(f"создан пользователь с email: {new_user.email}")
    except Exception as e:
        logger.error(f"ошибка создания пользователя {e}")
        raise HTTPException(status_code=500,
                             detail="Ошибка сервера")
    new_access_token = auth_service.create_access_token(new_user.email)
    new_refresh_token = auth_service.create_refresh_token(new_user.email)
    ResponseToken=Token(access_token=new_access_token,
                        refresh_token=new_refresh_token)
    return UserWithToken.model_validate(
        {**new_user.to_dict(),
        "token":ResponseToken}
    )


@router.post("/login", response_model=UserWithToken)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_session))-> UserWithToken:
    curent_user = await authenticate(session=db,email=user_data.email,password=user_data.password)
    new_access_token = auth_service.create_access_token(curent_user.email)
    new_refresh_token = auth_service.create_refresh_token(curent_user.email)
    ResponseToken = Token(access_token=new_access_token,
                        refresh_token=new_refresh_token)
    return UserWithToken.model_validate(
        {**curent_user.to_dict(),
        "token":ResponseToken}
    )


@router.post("/refresh",response_model=UserWithToken)
async def refresh_token(
    user_email: str = Depends(check_refresh),
    db: AsyncSession = Depends(get_session)
    )-> UserWithToken:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Данные не прошли проверку",
        headers={"WWW-Authenticate": "Bearer"},
    )
   
    user = await get_user_by_email(session=db,email=user_email)
    if not user:
        raise credentials_exception

    new_access_token = auth_service.create_access_token(user_email)
    new_refresh_token = auth_service.create_refresh_token(user_email)
    ResponseToken=Token.model_validate(
        {"access_token":new_access_token,
        "refresh_token":new_refresh_token}
    )
    print(ResponseToken)
    return UserWithToken.model_validate(
        {**user.to_dict(),
        "token":ResponseToken}
    )