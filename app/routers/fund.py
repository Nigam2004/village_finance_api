from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.models.transaction import FundTransaction
from app.schemas.finance import TransactionCreate, TransactionOut

router = APIRouter(prefix="/api/fund", tags=["transaction"])


@router.post("/transactions", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    if not db.get(Member, payload.member_id):
        raise HTTPException(status_code=404, detail="Member not found")
    data=payload.model_dump()
    data["total_amount_paid"] = (
    payload.principalPaid + payload.interestPaid
)
    item = FundTransaction(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/transactions", response_model=list[TransactionOut])
def list_transactions(member_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(FundTransaction).order_by(FundTransaction.transaction_date.desc(), FundTransaction.id.desc())
    if member_id is not None:
        stmt = stmt.where(FundTransaction.member_id == member_id)
    return db.scalars(stmt).all()
