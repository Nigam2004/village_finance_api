from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.models.loan import Loan
from app.schemas.finance import LoanCreate, LoanOut

router = APIRouter(prefix="/api/loans", tags=["Loans & Interest"])


def calculate_loan(principal: float, annual_rate: float, months: int, method: str):
    # simple: annual simple interest prorated for loan duration.
    # flat_monthly: the supplied rate is interpreted as a monthly percentage.
    if method == "simple":
        interest = principal * (annual_rate / 100) * (months / 12)
    else:
        interest = principal * (annual_rate / 100) * months
    total = principal + interest
    installment = total / months
    return round(interest, 2), round(total, 2)


@router.post("", response_model=LoanOut, status_code=201)
def create_loan(payload: LoanCreate, db: Session = Depends(get_db)):
    if not db.get(Member, payload.member_id):
        raise HTTPException(status_code=404, detail="Member not found")
    interest, total = calculate_loan(
        payload.principal, payload.annual_interest_rate, payload.duration_months, payload.interest_method
    )
    loan = Loan(
        **payload.model_dump(),
        interest_amount=interest,
        total_amount=total,
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@router.get("", response_model=list[LoanOut])
def list_loans(member_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Loan).order_by(Loan.loan_date.desc(), Loan.id.desc())
    if member_id is not None:
        stmt = stmt.where(Loan.member_id == member_id)
    if status:
        stmt = stmt.where(Loan.status == status)
    return db.scalars(stmt).all()


@router.patch("/{loan_id}/status", response_model=LoanOut)
def update_loan_status(loan_id: int, status: str, db: Session = Depends(get_db)):
    if status not in {"active", "closed", "overdue"}:
        raise HTTPException(status_code=422, detail="status must be active, closed, or overdue")
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.status = status
    db.commit()
    db.refresh(loan)
    return loan
