from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationAdminDB,
    DonationCreate,
    DonationCreateResponse,
    DonationMyDB,
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    summary='Получить список всех пожертвований',
    dependencies=[Depends(current_superuser)],
)
async def get_all(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationMyDB],
    summary='Получить список своих пожертвований',
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(session=session, user=user)


@router.post(
    '/',
    response_model=DonationCreateResponse,
    response_model_exclude_none=True,
    summary='Создать пожертвование',
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    db_donation = await donation_crud.create(
        donation, session, user=user, need_commit=False,
    )
    modified = invest(
        db_donation,
        await charity_project_crud.get_not_fully_invested(session),
    )
    session.add(db_donation)
    session.add_all(modified)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation
