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
from fastapi import FastAPI,Depends
from app.db.session import engine
from contextlib import asynccontextmanager
from app.utils import run_periodic_cleanup
import asyncio

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(run_periodic_cleanup())
    
    yield  # Здесь приложение работает
    await engine.dispose()
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="FastAPI_TaskManager",lifespan=lifespan)


app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")
logger.info("Приложение запущено")
logger.debug("Приложение запущено")