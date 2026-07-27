# app/services/donation.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.services.investment import invest


async def create_donation(
    donation: DonationCreate,
    session: AsyncSession,
    user: User,
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
