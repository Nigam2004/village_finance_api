
from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FundContribution(Base):
    __tablename__ = "fund_contributions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(150),nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2),nullable=False)
    contribution_date: Mapped[date] = mapped_column(Date,default=date.today,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False
    )
