from pydantic import BaseModel
from typing import Optional

class Section(BaseModel):
    section_id: Optional[int] = None
    course_id: int
    title: str
    content: Optional[str]
    description: Optional[str]
    external_resource_link: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_query_result(cls, section_id: int, course_id: int, title: str, content: Optional[str], 
                          description: Optional[str], external_resource_link: Optional[str]):
        return cls(section_id=section_id,
                   course_id=course_id,
                   title=title,
                   content=content,
                   description=description,
                   external_resource_link=external_resource_link
                   )
