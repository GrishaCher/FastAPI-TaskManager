from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Group(Base): 
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    group_description=Column(String, default="Рады новым участникам!")

    tasks = relationship("Task", back_populates="group")  # Задачи группы
    members = relationship("User", secondary="groups")  # Участники группы