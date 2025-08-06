from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError

from app.schemas.users import UserRegister, UserLogin, UserResponse,UserWithToken
from app.schemas.tokens import Token
from app.core.security import auth_service
from app.core.deps import check_refresh
from app.db.session import get_session
from app.crud.users import get_user_by_email, create_user,authenticate

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserWithToken)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_session))-> UserWithToken:
    try:
        await get_user_by_email(session=db,email=user_data.email)
    except HTTPException as e:
        raise HTTPException(status_code=400,
                             detail="Пользователь с таким email уже существует")
    try:
        new_user=await create_user(session=db,user_create=user_data)
    except:
        raise HTTPException(status_code=500,
                             detail="Ошибка сервера")
    new_access_token = auth_service.create_access_token(new_user.email)
    new_refresh_token = auth_service.create_refresh_token(new_user.email)
    ResponseToken=Token.model_validate(access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    return UserWithToken.model_validate(new_user,
                                        token=ResponseToken)



@router.post("/login", response_model=UserWithToken)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_session))-> UserWithToken:
    curent_user=await authenticate(session=db,email=user_data.email,password=user_data.password)
    new_access_token = auth_service.create_access_token(curent_user.email)
    new_refresh_token = auth_service.create_refresh_token(curent_user.email)
    ResponseToken=Token.model_validate(access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    return UserWithToken.model_validate(curent_user,
                                        token=ResponseToken)

@router.post("/refresh",response_model=UserResponse)
async def refresh_token(
    user_email: str = Depends(check_refresh),
    db: AsyncSession = Depends(get_session)
    )-> UserResponse:
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
    ResponseToken=Token.model_validate(access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    return UserWithToken.model_validate(user,
                                        token=ResponseToken)