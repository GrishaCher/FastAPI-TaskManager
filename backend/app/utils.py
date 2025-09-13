import aiosmtplib
from email.mime.text import MIMEText
from app.core.config import settings
from app.db.models import EmailVerificationDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from datetime import datetime
from app.db.session import get_session
from typing import AsyncGenerator
import asyncio

import logging

logger = logging.getLogger("app")

async def send_verification_email(email: str, token: str):
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    subject = "Подтверждение email"
    body = f"""
    Для завершения регистрации перейдите по ссылке:
    {verification_url}
    
    Ссылка действительна 24 часа.
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.SMTP_USER
    msg['To'] = email
    
    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD
        )
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
async def cleanup_expired_verifications()->int:
    """Удаляем просроченные верификационные записи"""
    session_gen: AsyncGenerator[AsyncSession, None] = get_session()
    session = await session_gen.__anext__()
    try:
        result = await session.execute(
            delete(EmailVerificationDB)
            .where(EmailVerificationDB.expires_at < datetime.now())
        )
        await session.commit()
        deleted_count = result.rowcount
        logger.info(f"Cleanup completed. Deleted {deleted_count} expired verifications")
        return deleted_count
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
async def run_periodic_cleanup():
    """Запускает периодическую очистку каждые 24 часа"""
    
    while True:
        try:
            await cleanup_expired_verifications()
            
            # Ожидаем 24 часа до следующего запуска
            await asyncio.sleep(24 * 60 * 60)  # 86400 секунд
            
        except Exception as e:
            logger.error(f"Periodic cleanup failed, retrying in 1 hour: {e}")
            # При ошибке ждем только час перед повторной попыткой
            await asyncio.sleep(60 * 60)