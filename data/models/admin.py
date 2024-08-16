from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class AdminAction(BaseModel):
    action_id: Optional[int] = None
    admin_id: Optional[int]
    action_type: str
    target_id: Optional[int]
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_query_result(cls, action_id: int, admin_id: Optional[int], action_type: str, target_id: Optional[int], timestamp: str):
        return cls(action_id=action_id,
                   admin_id=admin_id,
                   action_type=action_type,
                   target_id=target_id,
                   timestamp=timestamp
                   )

class RoleChangeRequest(BaseModel):
    email: str
    requested_role: str
    status: str = 'pending'
    requested_at: datetime = datetime.now