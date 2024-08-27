from pydantic import BaseModel, condecimal
from typing import Optional

class Course(BaseModel):
    title: str
    description: Optional[str]
    objectives: Optional[str]
    home_page_picture: Optional[bytes]
    is_premium: bool = False
    rating: condecimal(max_digits=3, decimal_places=2) = 0.00
    course_id: Optional[int] = None
    owner_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_query_result(cls, course_id: int, title: str, description: Optional[str], objectives: Optional[str],
                          home_page_picture: Optional[bytes], is_premium: bool, rating: condecimal(max_digits=3, decimal_places=2),
                          owner_id: Optional[int]):
        return cls(course_id=course_id,
                   title=title,
                   description=description,
                   objectives=objectives,
                   home_page_picture=home_page_picture,
                   is_premium=is_premium,
                   rating=rating,
                   owner_id=owner_id
                   )

#