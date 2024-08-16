from datetime import datetime
from typing import Optional
from data.database import query
from data.models.admin import RoleChangeRequest



def save_role_change_request(email:str, requested_role: str):
    user_query = query.table('users').select('user_id').eq('email', email).execute()
    user_data = user_query.data
    user_id = user_data[0]['user_id']
    data = {
        "user_id": user_query,
        "requested_role": requested_role,
        "status": "pending",
        "requested_at": datetime.now().isoformat()  # Format timestamp as ISO 8601
    }
    
    result = query.table('role_change_requests').insert(data).execute()
    return result
    

