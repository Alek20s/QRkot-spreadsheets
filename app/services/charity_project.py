# app/services/charity_project.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectCreate
from app.services.investment import invest


async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession,
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
