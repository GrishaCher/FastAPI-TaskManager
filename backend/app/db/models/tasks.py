from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import Base
from datetime import datetime

class Task(Base):  # Модель задач для таблицы в БД

    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey('users.id'))  # Для личных задач
    group_id = Column(Integer, ForeignKey('groups.id'))  # Для групповых задач
    # Связи
    owner = relationship("User", back_populates="tasks")
    group = relationship("Group", back_populates="tasks")