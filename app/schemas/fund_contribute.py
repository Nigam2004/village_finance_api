
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class FundContributionCreate(BaseModel):
    source: str = Field(min_length=1, max_length=150)
    amount: float = Field(gt=0)
    contribution_date: date = Field(default_factory=date.today)

class FundContributionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    amount: float
    contribution_date: date
    created_at: datetime
