from datetime import datetime
from typing import Optional
from data.database import query
from data.models.admin import RoleChangeRequest
from fastapi import HTTPException, status



def save_role_change_request(email:str, requested_role: str):
    user_query = query.table('users').select('user_id').eq('email', email).execute()
    user_data = user_query.data
    
    if not user_data or len(user_data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_id = user_data[0]['user_id']
    data = {
        "user_id": user_id,
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
        
    user_id = request.data[0]['user_id']
    query.table('role_change_requests').update({'status': 'approved'}).eq('id', request_id).execute()
    query.table('users').update({'role': 'teacher'}).eq('user_id', user_id).execute()

    return 'User added as teacher'
 
    
    
def reject_role_change_request(request_id:int):
    request = query.table('role_change_requests').select('*').eq('status','pending').execute()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role change request not found.'
        )
        
    user_id = request.data[0]['user_id']
    query.table('role_change_requests').update({'status': 'rejected'}).eq('id', request_id).execute()
    query.table('users').update({'role': 'student'}).eq('user_id', user_id).execute()

    return 'User was denied "teacher" account. User added as student.'


def remove_role(email:str):
    user_query = query.table('users').select('*').eq('email',email).execute()
    if not user_query.data or len(user_query.data) == 0:
        return False 
    user = user_query.data[0]
    
    if user.get('role') != 'teacher':
        return False  
    
    query.table('users').update({'role':'student'}).eq('email',email).execute()
    
    return True


def tag_creation(name:str):
    query.table('tags').insert({'name':name}).execute()
    
    return True
    
    