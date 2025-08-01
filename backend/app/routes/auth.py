from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError

from app.schemas.user import UserRegister, UserLogin, UserResponse,UserWithToken
from app.schemas.token import Token,RefreshTokenRequest
from app.db.models.users import User
from app.core.security import auth_service
from app.core.deps import oauth2_refresh_scheme
from app.db.session import get_session
from app.crud.users import get_user_by_email, create_user,authenticate

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_session))-> UserResponse:
    try:
        await get_user_by_email(session=db,email=user_data.email)
    except HTTPException as e:
        raise HTTPException(status_code=400,
                             detail="Пользователь с таким email уже существует")
    try:
        new_user=create_user(session=db,user_create=user_data)
    except:
        raise HTTPException(status_code=500,
                             detail="Ошибка сервера")
    new_access_token = auth_service.create_access_token(new_user.email)
    new_refresh_token = auth_service.create_refresh_token(new_user.email)
    return UserResponse(
        user=UserWithToken.model_validate(new_user,
                                          access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    )



@router.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_session))-> UserResponse:
    curent_user=await authenticate(session=db,email=user_data.email,password=user_data.password)
    new_access_token = auth_service.create_access_token(curent_user.email)
    new_refresh_token = auth_service.create_refresh_token(curent_user.email)
    return UserResponse(
        user=UserWithToken.model_validate(curent_user,
                                          access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    )

@router.post("/refresh",response_model=UserResponse)
async def refresh_token(
    token: str = Depends(oauth2_refresh_scheme),
    db: AsyncSession = Depends(get_session)
    )-> UserResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=auth_service.decode_token(token)
    except JWTError as e:
        #logger.errorf("ошибка JWT")  по хорошему
        raise HTTPException(401, detail=e)
   
    user_email = payload.get("sub")
    user = await get_user_by_email(session=db,email=user_email)
    if not user:
        raise credentials_exception

    new_access_token = auth_service.create_access_token(user_email)
    new_refresh_token = auth_service.create_refresh_token(user_email)
    
    return UserResponse(
        user=UserWithToken.model_validate(user,
                                          access_token=new_access_token,
                                          refresh_token=new_refresh_token)
    )
