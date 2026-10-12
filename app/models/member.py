from sqlalchemy import String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database import Base
from app.models.member import Member
from app.models.loan import Loan
from app.models.transaction import FundTransaction

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(20), default="Female")
    contact: Mapped[str | None] = mapped_column(String(40))
    address: Mapped[str | None] = mapped_column(String(255))
    occupation: Mapped[str | None] = mapped_column(String(120))
    join_date: Mapped[date] = mapped_column(Date, default=date.today)


    loans = relationship(
        "Loan",
        back_populates="member"
    )

    # Relationship with FundTransaction
    transactions = relationship(
        "FundTransaction",
        back_populates="member"
    )