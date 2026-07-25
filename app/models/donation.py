from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id'),
        nullable=True,
    )
    comment = Column(Text, nullable=True)

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return '{0}, user_id={1}, comment={2}'.format(
            base_repr, self.user_id, self.comment,
        )
