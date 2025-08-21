from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users_router import fastapi_users
from core.config import settings
from core.models import db_helper, User
from core.shemas.task import (
    TaskRead,
    TaskCreate,
    TaskUpdate,
)

from crud import tasks as tasks_crud

router = APIRouter(
    prefix=settings.api.v1.tasks,
    tags=["Tasks"],
)


@router.post("", response_model=TaskRead)
async def create_task(
    task_create: TaskCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user()),
):
    task = await tasks_crud.create_task(
        session=session,
        task_create=task_create,
        user_id=user.id,
    )
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user()),
):
    task = await tasks_crud.get_task_by_id(
        session=session,
        task_id=task_id,
    )
    if not task or task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.get("", response_model=list[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user()),
):
    task = await tasks_crud.get_all_tasks(session=session, user_id=user.id)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user()),
):
    task = await tasks_crud.get_task_by_id(session, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    task = await tasks_crud.update_task(
        session=session,
        task_id=task_id,
        task_update=task_update,
    )
    return task


@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user()),
):
    task = await tasks_crud.get_task_by_id(session, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    task = await tasks_crud.delete_task(
        session=session,
        task_id=task_id,
    )
    return task
