from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    father_name: str | None = Field(default=None, max_length=120)
    gender:str = Field(default="female", max_length=20)
    contact: str | None = Field(default=None, max_length=20)

  


class MemberUpdate(BaseModel):
    contact: str | None = Field(default=None, max_length=20)
    updated_date: date | None = None
 


class MemberOut(MemberCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    member_id:str
