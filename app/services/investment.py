from app.models.base import ProjectDonationBase


def invest(
    target: ProjectDonationBase,
    sources: list[ProjectDonationBase],
) -> list[ProjectDonationBase]:
    modified = []
    for source in sources:
        amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        source.add_investment(amount)
        target.add_investment(amount)
        modified.append(source)

        if target.fully_invested:
            break

    return modified
