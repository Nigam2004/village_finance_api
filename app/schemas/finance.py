from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class TransactionCreate(BaseModel):
    member_id: int
    loan_id:int
    transaction_type: Literal["deposit", "repayment"]
    principalPaid:float = Field(gt=0)
    interestPaid:float = Field(gt=0)
    # total_amount_paid: float = Field(gt=0)
    transaction_date: date = Field(default_factory=date.today)
    


class TransactionOut(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total_amount_paid: float = Field(gt=0)


class LoanCreate(BaseModel):
    member_id: int
    principal: float = Field(gt=0)
    annual_interest_rate: float = Field(ge=0, le=1000)
    duration_months: int = Field(gt=0, le=600)
    interest_method: Literal["simple", "flat_monthly"] = "simple"
    loan_date: date = Field(default_factory=date.today)
    note: str | None = Field(default=None, max_length=500)


class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    member_id: int
    principal: float
    annual_interest_rate: float
    duration_months: int
    interest_method: str=Field(default="simple")
    interest_amount: float
    total_amount: float
    loan_date: date
    status: str
    note: str | None
    transaction: list[TransactionOut]


class ExpenseCreate(BaseModel):
    expense_type: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    amount: float = Field(gt=0)
    expense_date: date = Field(default_factory=date.today)


class ExpenseOut(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
