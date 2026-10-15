
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.fund_contribution import FundContribution
from app.schemas.fund_contribute import (
    FundContributionCreate,
    FundContributionOut,
)

router = APIRouter(
    prefix="/api/fund-contributions",
    tags=["Fund Contributions"]
)


@router.post("/", response_model=FundContributionOut, status_code=201)
def create_contribution(
    data: FundContributionCreate,
    db: Session = Depends(get_db)
):
    contribution = FundContribution(
        source=data.source.strip(),
        amount=data.amount,
        contribution_date=data.contribution_date
    )

    if not contribution.source:
        raise HTTPException(
            status_code=422,
            detail="Source/contributor cannot be empty"
        )

    db.add(contribution)
    db.commit()
    db.refresh(contribution)

    return contribution


@router.get("/", response_model=list[FundContributionOut])
def get_contributions(db: Session = Depends(get_db)):
    return (
        db.query(FundContribution)
        .order_by(FundContribution.contribution_date.desc())
        .all()
    )


@router.get("/{contribution_id}", response_model=FundContributionOut)
def get_contribution(
    contribution_id: int,
    db: Session = Depends(get_db)
):
    contribution = db.query(FundContribution).filter(
        FundContribution.id == contribution_id
    ).first()

    if contribution is None:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )

    return contribution


@router.delete("/{contribution_id}", status_code=204)
def delete_contribution(
    contribution_id: int,
    db: Session = Depends(get_db)
):
    contribution = db.query(FundContribution).filter(
        FundContribution.id == contribution_id
    ).first()

    if contribution is None:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )

    db.delete(contribution)
    db.commit()
