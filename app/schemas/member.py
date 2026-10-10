from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    father_name: str | None = Field(default=None, max_length=120)
    mobile: str | None = Field(default=None, max_length=20)
    village: str | None = Field(default=None, max_length=120)
    address: str | None = None
    occupation: str | None = Field(default=None, max_length=120)
    joining_date: date = Field(default_factory=date.today)
    opening_balance: float = Field(default=0, ge=0)


class MemberUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    father_name: str | None = None
    mobile: str | None = None
    village: str | None = None
    address: str | None = None
    occupation: str | None = None
    joining_date: date | None = None
    opening_balance: float | None = Field(default=None, ge=0)


class MemberOut(MemberCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
