from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDBase:

    def __init__(self, model: type) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[object]:
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list:
        return (await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )).scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user=None,
        need_commit: bool = True,
    ) -> object:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data.setdefault('invested_amount', 0)
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if need_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> object:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if (
            hasattr(db_obj, 'full_amount') and
            hasattr(db_obj, 'invested_amount') and
            db_obj.full_amount == db_obj.invested_amount
        ):
            db_obj.close()
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> object:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
