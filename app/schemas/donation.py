from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationCreateResponse(BaseModel):
    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        from_attributes = True


class DonationDB(DonationBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class DonationAdminDB(DonationDB):
    user_id: Optional[int] = None


class DonationMyDB(BaseModel):
    id: int
    comment: Optional[str] = None
    full_amount: int
    create_date: datetime

    class Config:
        from_attributes = True
