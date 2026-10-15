from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base
# from app.models.loan import Loan
# from app.models.transaction import FundTransaction

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_acc: Mapped[str | None] = mapped_column(String(30),unique=True,index=True,nullable=True
    )
    name: Mapped[str] = mapped_column(String(120))
    father_name:Mapped[str] = mapped_column(String(120))
    gender: Mapped[str] = mapped_column(String(20), default="Female")
    contact: Mapped[str | None] = mapped_column(String(40))
    join_date: Mapped[date] = mapped_column(Date, default=date.today)
    updated_date: Mapped[date] = mapped_column(Date, default=date.today)

    loans: Mapped[list["Loan"]] = relationship(
    "Loan",
    back_populates="member"
    )
   