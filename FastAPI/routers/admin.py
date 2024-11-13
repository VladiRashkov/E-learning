from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from data.models.user import User
from common.auth import get_current_user
from services.admin_services import approve_role_change_request, reject_role_change_request,\
    get_role_change_requests, remove_role, tag_creation, assign

admin_router = APIRouter(prefix='/admin', tags=['admin'])
    
@admin_router.get('/role_change_request')
def get_requests(current_user:User = Depends(get_current_user)):
    role = current_user['role']
    if role != 'admin':
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admins can access role change requests.'
        )
        
    result = get_role_change_requests()
    
    return result
        
        
@admin_router.post('/approve_role_change/{request_id}')
def approve_request(request_id: int, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can approve role change requests."
        )
    approve_role_change_request(request_id)
    return {"message": "Role change request approved."}


@admin_router.post('/reject_role_change/{request_id}')
def reject_request(request_id: int, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != "admin":
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can reject role change requests."
        )
    reject_role_change_request(request_id)
    return {"message": "Role change request rejected."}

@admin_router.put('/remove_teacher_role/{email}')
def remove_access(email:str, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can reject role change requests."
        )
    result = remove_role(email)
    if result:
        return {"message": 'The user has had the "teacher" role suspended.'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or the user is not a teacher."
        )
        
        
@admin_router.post('/tag')
def create_tag(name:str, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != "admin":
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create tags."
        )
        
    tag_creation(name)
    return f'Tag {name} added '

@admin_router.post('assign_tag')
def to_course(tag_name:str, course_name:str, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != "admin":
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can assign tags."
        )
        
    assign(tag_name, course_name)
    
    return 'Tag assigned to course!'