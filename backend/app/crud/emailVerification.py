from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.core.security import auth_service
from app.db.models import EmailVerificationDB
from datetime import datetime, timedelta
from app.schemas.users import UserRegister
import secrets

import logging

logger = logging.getLogger("app")


async def create_verification(
    *, session: AsyncSession, user_data: UserRegister
) -> EmailVerificationDB:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=24)
    try:
        verification = EmailVerificationDB(
            email=user_data.email,
            username=user_data.username,
            token=token,
            expires_at=expires_at,
            hashed_password=auth_service.get_password_hash(user_data.password),
        )
        session.add(verification)
        await session.commit()
    except Exception as e:
        logger.error(f"Error creating EmailVerification: {e}")
        raise HTTPException(
            status_code=400,
            detail="Wrong creditinals",
        )
    return verification


async def get_verification(
    *, session: AsyncSession, token: str
) -> EmailVerificationDB | None:
    result = await session.execute(
        select(EmailVerificationDB).where(EmailVerificationDB.token == token)
    )
    verification = result.scalar_one_or_none()

    if not verification:
        raise HTTPException(404, "Invalid verification token")

    if verification.is_used:
        raise HTTPException(400, "Token already used")

    if verification.expires_at < datetime.now():
        raise HTTPException(400, "Verification token expired")
    return verification
