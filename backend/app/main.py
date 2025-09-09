from app.core.logger import setup_logger # сначала импортирую логгер
import logging
setup_logger(
    log_level=logging.DEBUG,
    log_file="app.log",
    console_log=True
)

from app.patches.bcrypt_fix import * # потом импортирую патч bcrypt для корректной работы passlib

from app.core.config import settings # остальные импорты
from app.routes import users,auth,tasks
from fastapi import FastAPI
from app.db.session import engine
from fastapi import Request, HTTPException
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("app")

app = FastAPI(title="FastAPI_TaskManager")
@app.on_event("shutdown")
async def shutdown_db_connection():
    await engine.dispose()
app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")
logger.info("Приложение запущено")
logger.debug("Приложение запущено")