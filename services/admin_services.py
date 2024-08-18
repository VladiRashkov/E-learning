from datetime import datetime
from typing import Optional
from data.database import query
from data.models.admin import RoleChangeRequest
from fastapi import HTTPException, status



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
    
def get_role_change_requests():
    return query.table('role_change_requests').select('*').eq('status','pending').execute()

    
def approve_role_change_request(request_id:int):
    request = query.table('role_change_requests').select('*').eq('status','pending').execute()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role change request not found.'
        )
        
    request_data = request.data
    request_data['status'] = 'approved'
    
    
def reject_role_change_request(request_id:int):
    request = query.table('role_change_requests').select('*').eq('status','pending').execute()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role change request not found.'
        )
        
        
    request_data = request.data
    
    
    request_data['status'] = 'rejected'
