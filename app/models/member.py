from datetime import date
from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

from app.models.loan import Loan
from app.models.transaction import FundTransaction


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    father_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    village: Mapped[str | None] = mapped_column(String(120), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    occupation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    joining_date: Mapped[date] = mapped_column(Date, default=date.today)
    opening_balance: Mapped[float] = mapped_column(default=0)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    loans: Mapped[list["Loan"]] = relationship(back_populates="member")
    transactions: Mapped[list["FundTransaction"]] = relationship(back_populates="member")
