from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserRegister, UserWithToken
from app.schemas.tokens import Token
from app.core.security import auth_service
from app.core.deps import check_refresh
from app.db.session import get_session
from app.crud.users import (
    get_user_by_email,
    create_user,
    authenticate,
    get_user_by_username,
)
from app.crud.emailVerification import create_verification, get_verification
from app.utils import send_verification_email

from sqlalchemy.ext.asyncio import AsyncSession

import logging


logger = logging.getLogger("app")


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=dict, status_code=202)
async def register(
    user_data: UserRegister, db: AsyncSession = Depends(get_session)
) -> dict:
    logger.debug(f"начало регистрации пользователя: {user_data}")

    if await get_user_by_email(session=db, email=user_data.email):
        raise HTTPException(
            status_code=401, detail="Пользователь с таким email уже существует"
        )

    logger.debug(f"пользователя с таким email {user_data.email} пока нет")
    if await get_user_by_username(session=db, username=user_data.username):
        raise HTTPException(
            status_code=401, detail="Пользователь с таким именем уже существует"
        )
    logger.debug(f"пользователя с таким username {user_data.username} пока нет")

    verification = await create_verification(session=db, user_data=user_data)

    # Отправляем email с ссылкой подтверждения
    try:
        await send_verification_email(verification.email, verification.token)
    except:
        pass
    return {"message": f"email has been sent to {verification.email}"}


@router.post("/verify-email/{token}", response_model=UserWithToken)
async def verify_email(
    token: str, db: AsyncSession = Depends(get_session)
) -> UserWithToken:
    verification = await get_verification(token=token, session=db)
    if verification is None:
        raise HTTPException(status_code=400, detail="The link expired")

    try:
        new_user = await create_user(
            user_email=verification.email,
            password_hash=verification.hashed_password,
            username=verification.username,
            session=db,
        )
        logger.info(f"создан пользователь с email: {new_user.email}")
    except Exception as e:
        logger.error(f"ошибка создания пользователя {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")
    new_access_token = auth_service.create_access_token(new_user.email)
    new_refresh_token = auth_service.create_refresh_token(new_user.email)
    ResponseToken = Token(
        access_token=new_access_token, refresh_token=new_refresh_token
    )
    return UserWithToken.model_validate({**new_user.to_dict(), "token": ResponseToken})


@router.post("/login", response_model=Token)
async def login(
    user_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
) -> Token:
    curent_user = await authenticate(
        session=db, email=user_data.username, password=user_data.password
    )
    new_access_token = auth_service.create_access_token(curent_user.email)
    new_refresh_token = auth_service.create_refresh_token(curent_user.email)
    ResponseToken = Token(
        access_token=new_access_token, refresh_token=new_refresh_token
    )
    return ResponseToken


@router.post("/refresh", response_model=Token)
async def refresh_token(
    user_email: str = Depends(check_refresh), db: AsyncSession = Depends(get_session)
) -> Token:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Данные не прошли проверку",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await get_user_by_email(session=db, email=user_email)
    if not user:
        raise credentials_exception

    new_access_token = auth_service.create_access_token(user_email)
    new_refresh_token = auth_service.create_refresh_token(user_email)
    ResponseToken = Token.model_validate(
        {"access_token": new_access_token, "refresh_token": new_refresh_token}
    )
    return ResponseToken
