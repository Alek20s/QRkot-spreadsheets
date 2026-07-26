# app/crud/charity_project.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> int:
        result = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return result.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list:
        result = await session.execute(
            select(self.model).where(self.model.fully_invested.is_(True))
        )
        projects = result.scalars().all()
        return sorted(
            projects,
            key=lambda p: p.close_date - p.create_date,
        )


charity_project_crud = CRUDCharityProject(CharityProject)
