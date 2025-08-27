from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import Base,SerializerMixin
from datetime import datetime

class Task(Base,SerializerMixin):  # Модель задач для таблицы в БД

    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    deadline = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))  # Для личных задач
    group_id = Column(Integer, ForeignKey('groups.id'),nullable=True)  # Для групповых задач
    # Связи
    owner = relationship("User", back_populates="tasks")
    group = relationship("Group", back_populates="tasks")