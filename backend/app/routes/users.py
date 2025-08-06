from fastapi import APIRouter, Depends, HTTPException

from app.schemas.users import UserResponse,UserInUpdate
from app.schemas.tokens import Token
from app.db.models import User
from app.core.security import auth_service
from app.core.deps import get_current_user
from app.db.session import get_session
from app.crud.users import update_user


router = APIRouter(tags=["user"])

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_current_user)  
)-> UserResponse:
    """
    Отправляем клиенту данные авторизированного пользователя
    """
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь неактивен")
    return UserResponse.model_validate(current_user)

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserInUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_session)
)-> UserResponse:
    if update_user is None:
        raise HTTPException(status_code=401,
                             detail="Данные не переданы")
    new_user=update_user(session=db,db_user=current_user,user_in=update_data)
    return UserResponse.model_validate(new_user)