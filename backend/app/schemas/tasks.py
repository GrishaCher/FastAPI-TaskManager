from app.schemas.base import BaseModelWithConfig
from datetime import datetime
from typing import Optional, List


class TaskCreate(BaseModelWithConfig):
    title: str
    deadline: Optional[datetime] = None


class TaskResponse(TaskCreate):
    is_completed: bool
    created_at: datetime
    id: int


class PaginatedTasksResponse(BaseModelWithConfig):
    tasks: List[TaskResponse]
    total: int
    skip: int
    limit: int


class TaskInUpdate(TaskCreate):
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None
