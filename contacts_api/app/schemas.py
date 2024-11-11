from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
