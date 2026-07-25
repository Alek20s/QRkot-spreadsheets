from sqlalchemy import Column, String, Text

from app.models.base import ProjectDonationBase


class CharityProject(ProjectDonationBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return '{0}, name={1}'.format(base_repr, self.name)
