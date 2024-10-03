from pydantic import BaseModel, condecimal
from typing import Optional

from pydantic import BaseModel, Field


class CreateCourse(BaseModel):
    __tablename__ = 'courses'
    title:str
    description:str
    home_page_picture:str
    is_premium:bool = False
    rating: float
    objectives:str
    
    @classmethod
    def from_query_result(cls, title: str, description:str, home_page_picture:str, is_premium:bool, rating: float, objectives:str):
        return cls(title=title,
                   description=description,
                   home_page_picture=home_page_picture,
                   is_premium=is_premium,
                   rating=rating,
                   objectives=objectives
                   )
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class UpdateCourse(BaseModel):
    title: str = ''
    description: Optional[str] = ''
    home_page_picture: Optional[str] = ''
    is_premium: bool = False
    rating: condecimal(max_digits=3, decimal_places=2) = 0.00
    objectives: Optional[str] = ''
    
    
    @classmethod
    def from_query_result(cls, title: str, description:str, home_page_picture:str, is_premium:bool, rating: float, objectives:str):
        return cls(title=title,
                   description=description,
                   home_page_picture=home_page_picture,
                   is_premium=is_premium,
                   rating=rating,
                   objectives=objectives
                   )
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)