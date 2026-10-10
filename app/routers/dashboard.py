from fastapi import APIRouter, Depends
from sqlalchemy import select, func, case
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.models.loan import Loan
from app.models.expense import Expense
from app.models.transaction import FundTransaction

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    member_count = db.scalar(select(func.count(Member.id))) or 0
    total_principal = db.scalar(select(func.coalesce(func.sum(Loan.principal), 0))) or 0
    interest_expected = db.scalar(select(func.coalesce(func.sum(Loan.interest_amount), 0))) or 0
    expenses_total = db.scalar(select(func.coalesce(func.sum(Expense.amount), 0))) or 0
    deposits = db.scalar(select(func.coalesce(func.sum(FundTransaction.amount), 0)).where(FundTransaction.transaction_type == "deposit")) or 0
    repayments = db.scalar(select(func.coalesce(func.sum(FundTransaction.amount), 0)).where(FundTransaction.transaction_type == "repayment")) or 0
    loans_out = db.scalar(select(func.coalesce(func.sum(Loan.principal), 0)).where(Loan.status == "active")) or 0
    return {
        "total_members": member_count,
        "total_loans_principal": round(float(total_principal), 2),
        "expected_interest": round(float(interest_expected), 2),
        "total_expenses": round(float(expenses_total), 2),
        "total_deposits": round(float(deposits), 2),
        "total_repayments": round(float(repayments), 2),
        "active_loan_principal": round(float(loans_out), 2),
    }
