from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> list:
        return (await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )).scalars().all()


donation_crud = CRUDDonation(Donation)
