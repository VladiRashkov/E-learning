from pydantic import BaseModel, Field


class CreateCourse(BaseModel):
    title:str
    description:str
    home_page_picture:str
    is_premium:bool = False
    rating: float
    objectives:str
    
class ChangePassword(BaseModel):
    password:str = Field(..., write_only=True)
    
    class Config:
        schema_extra = {
            "example": {
                "password": "********"  # This is just an example. It can be any placeholder.
            }
        }