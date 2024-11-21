from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=15)
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)
    first_name: str = Field(..., max_length=50)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str = Field(..., max_length=50)

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Contact(BaseModel):
    id: int
    first_name: str = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=15)
    email: EmailStr

    class Config:
        from_attributes = True 