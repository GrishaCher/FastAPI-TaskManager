from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func

from fastapi import HTTPException

from app.db.models import Task
from app.schemas.tasks import TaskCreate,TaskInUpdate,PaginatedTasksResponse

import logging
logger = logging.getLogger("app")

async def create_task(*, session: AsyncSession, user_id: int,task_data:TaskCreate) -> Task:

    logger.debug(f"попытка создать задачу {task_data.title} пользователем с id: {user_id}")
    db_task = Task(
        title = task_data.title,
        deadline = task_data.deadline,
        user_id = user_id
        #group_id = Column(Integer, ForeignKey('groups.id'),nullable=True)  
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    logger.info(f"Задача {db_task.title} пользователя с id: {db_task.user_id} сохранён")
    return db_task


async def update_task(*, session: AsyncSession, user_id: int, task_id:int, task_in:TaskInUpdate) -> Task:
    task_data = task_in.model_dump(exclude_unset=True)
    if not task_data:
        logger.debug("нет данных обновления")
        raise HTTPException(
                status_code=400,
                detail="поля не выбранны",
            ) 
    task=await get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    logger.info(f"задача {task.to_dict()}  сохранена")
    return task


async def get_user_tasks(*, session: AsyncSession, user_id:int,skip,limit,completed) -> PaginatedTasksResponse | None:
    query = select(Task).where(Task.user_id == user_id) 
    if completed is not None:
        query = query.where(Task.is_completed == completed)
    result = await session.execute(query.offset(skip).limit(limit))
    tasks = result.scalars().all()
    
    total_result = await session.execute(
        select(func.count()).where(Task.user_id == user_id)
    )
    total = total_result.scalar()
    
    return PaginatedTasksResponse.model_validate(
        {
        "tasks": tasks,
        "total": total,
        "skip": skip,
        "limit": limit,
        }
    )

async def get_task_by_id(*, session: AsyncSession, task_id: int, user_id:int) -> Task | None:
    current_task = await session.get(Task, task_id)
    
    if current_task.user_id != user_id:  
        raise HTTPException(status_code=403, detail="Access denied")
    
    return current_task

async def delete_task_by_id(*, session: AsyncSession, task_id: int, user_id:int) -> dict:
    logger.info(f"попытка удачить задачу с id: {task_id}")
    task=await get_task_by_id(session=session,user_id=user_id,task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    
    return {"message": f"удалена задача с id: {task_id}"}
