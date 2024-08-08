from pydantic import BaseModel, constr, EmailStr
from typing import Optional

TUsername = constr(pattern='^\\w{2,30}$')

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    
    @classmethod
    def from_query_result(cls, id, email, first_name, last_name, password):
        return cls(id=id,
                   email=email,
                   first_name=first_name,
                   last_name=last_name,
                   password=password
                   )
    
    
class Admin(User):
    pass

class Teacher(User):
    pass

class Student(User):
    pass

class LoginData(BaseModel):
    username: TUsername
    password: str