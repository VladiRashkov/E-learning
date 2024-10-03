from pydantic import BaseModel, Field


class ChangePassword(BaseModel):
    password:str = Field(..., write_only=True)
    
    class Config:
        schema_extra = {
            "example": {
                "password": "********"  # This is just an example. It can be any placeholder.
            }
        }