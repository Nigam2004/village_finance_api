from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base



class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    principal: Mapped[float] = mapped_column()
    annual_interest_rate: Mapped[float] = mapped_column(default=0)  # percent per year
    duration_months: Mapped[int] = mapped_column()
    interest_method: Mapped[str] = mapped_column(String(20), default="simple")  # simple or flat_monthly
    interest_amount: Mapped[float] = mapped_column()
    total_amount: Mapped[float] = mapped_column()
    loan_date: Mapped[date] = mapped_column(Date, default=date.today)
    status: Mapped[str] = mapped_column(String(20), default="active")
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    member: Mapped["Member"] = relationship(
    "Member",
    back_populates="loans"
)