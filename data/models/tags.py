from pydantic import BaseModel
from typing import Optional

class Tag(BaseModel):
    tag_id: Optional[int] = None
    name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_query_result(cls, tag_id: int, name: str):
        return cls(tag_id=tag_id, name=name)
