from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ProjectDonationBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
    )
    full_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('full_amount > 0', name='full_amount_positive'),
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='invested_amount_in_range',
        ),
        default=0,
    )
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now,
    )
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def close(self) -> None:
        self.fully_invested = True
        self.close_date = datetime.now()

    def add_investment(self, amount: int) -> None:
        self.invested_amount += amount
        if self.invested_amount == self.full_amount:
            self.close()

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}('
            f'id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date})'
        )
