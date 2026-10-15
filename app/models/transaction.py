from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
# from app.models.member import Member


class FundTransaction(Base):
    __tablename__ = "fund_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), index=True)
    transaction_type: Mapped[str] = mapped_column(String(20))  # deposit or repayment
    tota_amount_paid: Mapped[float] = mapped_column()
    principalPaid:Mapped[float] = mapped_column()
    interestPaid:Mapped[float] = mapped_column()
    transaction_date: Mapped[date] = mapped_column(Date, default=date.today)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    member: Mapped["Member"] = relationship("Member",back_populates="transactions")
