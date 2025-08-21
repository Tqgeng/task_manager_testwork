from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.shemas.task import TaskCreate, TaskUpdate


async def create_task(
    session: AsyncSession,
    task_create: TaskCreate,
    user_id: int,
) -> Task:
    task = Task(**task_create.model_dump(), user_id=user_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    return await session.get(Task, task_id)


async def get_all_tasks(
    session: AsyncSession,
    user_id: int | None = None,
) -> Sequence[Task]:
    stmt = select(Task).order_by(Task.id)
    if user_id is not None:
        stmt = stmt.where(Task.user_id == user_id)
    result = await session.scalars(stmt)
    return result.all()


async def update_task(
    session: AsyncSession,
    task_update: TaskUpdate,
    task_id: int,
) -> Task | None:
    task = await session.get(Task, task_id)
    if not task:
        return None
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    task = await session.get(Task, task_id)
    if not task:
        return None
    await session.delete(task)
    await session.commit()
    return task
