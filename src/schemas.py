from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    email: EmailStr = Field(max_length=50)
    phone_number: str = Field(max_length=20)
    birthday: Optional[date]


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=30)
    surname: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    birthday: date | None = None
