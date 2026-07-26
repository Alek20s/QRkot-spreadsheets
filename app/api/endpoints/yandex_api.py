# app/api/endpoints/yandex_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.crud.charity_project import charity_project_crud
from app.services.yandex_api import create_simple_report

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
    summary='Сформировать отчёт и загрузить его на Яндекс.Диск',
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    client: YandexDiskClient = Depends(get_yandex_client),
) -> str:
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    if not projects:
        raise HTTPException(
            status_code=404,
            detail='Нет закрытых проектов для отчёта.',
        )
    try:
        return await create_simple_report(
            projects, client, settings.report_format,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
