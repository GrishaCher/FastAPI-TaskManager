from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import Base,SerializerMixin
from datetime import datetime

from sqlalchemy import Enum
from enum import Enum as PyEnum
class Group(Base,SerializerMixin): 
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30),unique=True)
    created_at = Column(DateTime, default=datetime.now)
    group_description=Column(String(300), default="Рады новым участникам!")

    tasks = relationship("Task", back_populates="group")  # Задачи группы
    members = relationship("User", secondary="user_groups",back_populates="groups")  # Участники группы
class GroupRole(PyEnum):
    ADMIN = "admin"
    MEMBER = "member"

class UserGroup(Base):
    __tablename__ = "user_groups"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    role = Column(Enum(GroupRole), default=GroupRole.MEMBER)
    