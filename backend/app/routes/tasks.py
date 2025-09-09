from fastapi import APIRouter, Depends, HTTPException

from app.schemas.tasks import TaskResponse,PaginatedTasksResponse,TaskCreate,TaskInUpdate
from app.db.models import User
from app.core.deps import get_current_user
from app.db.session import get_session
from app.crud.tasks import get_task_by_id,get_user_tasks,create_task,update_task,delete_task_by_id

from typing import Optional
import logging
logger = logging.getLogger("app")

router = APIRouter(tags=["tasks"])

@router.get("/", response_model=PaginatedTasksResponse)
async def read_user_tasks(
    db=Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,  
    limit: int = 10,  
    completed: Optional[bool] = None 
)-> PaginatedTasksResponse:
    """
    Отправляем задачи авторизированному пользователю
    """
    logger.debug(f"Попытка получить задачи пользователя с id: {current_user.id}")
    tasks=await get_user_tasks(
        session=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed
    )
    if tasks is None:
        raise HTTPException(status_code=404,
                             detail="Tasks not found")
    if tasks.tasks!=[]:
        logger.info(f"Получены задачи {tasks.tasks[0]} - {tasks.tasks[len(tasks.tasks)-1]} пользователя с id: {current_user.id}")
    else:
        logger.info(f"Нет задач у пользователя с id: {current_user.id}")
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def read_user_task_by_id(
    task_id:int,
    db=Depends(get_session),
    current_user: User = Depends(get_current_user),
)-> TaskResponse:
    task=await get_task_by_id(session=db,task_id=task_id,user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)

@router.post("/", response_model=TaskResponse)
async def add_new_task(
    task_data: TaskCreate,
    db=Depends(get_session),
    current_user: User = Depends(get_current_user),
)-> TaskResponse:
    task=await create_task(session=db,user_id=current_user.id,task_data=task_data)
    if not task:
        raise HTTPException(status_code=400, detail="Bad Request")
    return TaskResponse.model_validate(task)
@router.patch("/{task_id}", response_model=TaskResponse)
async def update_user_task(
    task_id:int,
    task_data: TaskInUpdate,
    db=Depends(get_session),
    current_user: User = Depends(get_current_user),
)-> TaskResponse:
    task=await update_task(session=db, user_id=current_user.id, task_id=task_id, task_in=task_data)
    if not task:
        raise HTTPException(status_code=400, detail="Bad Request")
    return TaskResponse.model_validate(task)
@router.delete("/{task_id}", response_model=dict)
async def delete_user_task(
    task_id:int,
    db=Depends(get_session),
    current_user: User = Depends(get_current_user),
)-> TaskResponse:
    delete_message=await delete_task_by_id(session=db,user_id=current_user.id,task_id=task_id)
    if not delete_message:
        raise HTTPException(status_code=400, detail="Bad Request")
    return delete_message