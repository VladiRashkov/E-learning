from pydantic import BaseModel, condecimal
from typing import Optional

class Enrollment(BaseModel):
    enrollment_id: Optional[int] = None
    student_id: int
    course_id: int
    progress: condecimal(max_digits=5, decimal_places=2) = 0.00
    is_subscribed: bool = True

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_query_result(cls, enrollment_id: int, student_id: int, course_id: int, progress: condecimal(max_digits=5, decimal_places=2),
                          is_subscribed: bool):
        return cls(enrollment_id=enrollment_id,
                   student_id=student_id,
                   course_id=course_id,
                   progress=progress,
                   is_subscribed=is_subscribed
                   )
