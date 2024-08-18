from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from data.models.user import User
from common.auth import get_current_user
from services.admin_services import approve_role_change_request, reject_role_change_request

admin_router = APIRouter(prefix='/admin', tags=['admin'])

@admin_router.get('/role_change_request')
def get_requests(current_user:User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admins can access role change requests.'
        )
        
        
@admin_router.post('/approve_role_change/{request_id}')
def approve_request(request_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can approve role change requests."
        )
    approve_role_change_request(request_id)
    return {"message": "Role change request approved."}


@admin_router.post('/reject_role_change/{request_id}')
def reject_request(request_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can reject role change requests."
        )
    reject_role_change_request(request_id)
    return {"message": "Role change request rejected."}