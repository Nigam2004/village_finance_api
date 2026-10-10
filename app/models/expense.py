from datetime import date
from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    expense_type: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(500))
    amount: Mapped[float] = mapped_column()
    expense_date: Mapped[date] = mapped_column(Date, default=date.today)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
