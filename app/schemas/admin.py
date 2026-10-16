from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class AdminRegister(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator("full_name")
    @classmethod
    def strip_full_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Full name must not be empty")
        return value

    @model_validator(mode="after")
    def passwords_must_match(self) -> "AdminRegister":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
