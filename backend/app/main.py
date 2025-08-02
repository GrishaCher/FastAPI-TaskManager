from app.core.config import settings
from app.routes import users,auth
from fastapi import FastAPI
print(settings.sqlalchemyURL)

app = FastAPI(title="FastAPI_TaskManager")
app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/users")