from pydantic import BaseModel, constr, EmailStr, field_validator
from typing import Optional
from enum import Enum
from fastapi import HTTPException, status, Query

class UserRole(str, Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    photo: Optional[str] | None=None
    role: UserRole
    phone_number: Optional[str] | None
    linkedin_account: Optional[str] | None
    
    @classmethod
    def from_query_result(cls, id: int, email: str, first_name: str, last_name: str, password: str):
        return cls(id=id,
                   email=email,
                   first_name=first_name,
                   last_name=last_name,
                   password=password
                   )
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class LoginData(BaseModel):
    email: EmailStr = Query(..., example="", alias="email")
    password: str = Query(..., example="", alias="password")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "",
                "password": ""
            }
        }

    
class UpdateUserData(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    photo:Optional[str]
    role:Optional[str]
    phone_number:Optional[str]
    linkedin_account:Optional[str]
    
    @field_validator('role')
    def normalize_role(cls, v):
        if v:
            return v.lower()  # Convert the role to lowercase before processing
        return v

