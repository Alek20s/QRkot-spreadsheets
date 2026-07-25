from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_can_be_deleted,
    check_project_can_be_updated,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Получить список всех проектов',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать новый проект',
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate = Depends(check_name_duplicate),
    session: AsyncSession = Depends(get_async_session),
):
    db_project = await charity_project_crud.create(
        project, session, need_commit=False,
    )
    modified = invest(
        db_project, await donation_crud.get_not_fully_invested(session),
    )
    session.add(db_project)
    session.add_all(modified)
    await session.commit()
    await session.refresh(db_project)
    return db_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Обновить проект',
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    update_data: CharityProjectUpdate,
    db_project=Depends(check_project_can_be_updated),
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.update(db_project, update_data, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Удалить проект',
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    db_project=Depends(check_project_can_be_deleted),
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.remove(db_project, session)
