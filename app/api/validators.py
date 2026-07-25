from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


async def check_project_exists(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    db_project = await charity_project_crud.get(project_id, session)
    if db_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден',
        )
    return db_project


async def check_project_can_be_updated(
    update_data: CharityProjectUpdate,
    db_project=Depends(check_project_exists),
    session: AsyncSession = Depends(get_async_session),
):
    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать',
        )
    if (
        update_data.full_amount is not None
        and update_data.full_amount < db_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить сумму меньше уже вложенной',
        )
    if update_data.name is not None:
        existing_id = await charity_project_crud.get_project_id_by_name(
            update_data.name, session,
        )
        if existing_id is not None and existing_id != db_project.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует',
            )
    return db_project


def check_project_can_be_deleted(
    db_project=Depends(check_project_exists),
):
    if db_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже внесены средства, удаление невозможно',
        )
    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя удалить',
        )
    return db_project


async def check_name_duplicate(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectCreate:
    project_id = await charity_project_crud.get_project_id_by_name(
        project.name, session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует',
        )
    return project
