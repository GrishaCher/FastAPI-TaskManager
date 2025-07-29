from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.models.base import Base
from datetime import datetime

class User(Base):  # Модель пользователей для таблицы в БД

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, nullable=False,unique=True)
    created_at = Column(DateTime, default=datetime.now)
    hashed_password=Column(String)

    tasks=relationship("Task", back_populates="owner")
    groups = relationship("Group", secondary="user_groups") 