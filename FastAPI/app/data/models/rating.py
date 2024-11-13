from pydantic import BaseModel, conint
from typing import Optional


class Rating(BaseModel):
    rating_id: Optional[int] = None
    student_id: int
    course_id: int
    score: conint(ge=1, le=10)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_query_result(cls, rating_id: int, student_id: int, course_id: int, score: int):
        return cls(rating_id=rating_id,
                   student_id=student_id,
                   course_id=course_id,
                   score=score
                   )
