from fastapi import APIRouter, HTTPException, status
from FastAPI.services.enrollment_services import enroll_in_course, part_of_courses
from fastapi import Depends
from FastAPI.data.models.user import User
from FastAPI.common.auth import get_current_user


enrollment_router = APIRouter(prefix='/enroll', tags=['enrollment'])

@enrollment_router.put('/add_user/{user_id}')
def add_user_to_course(user_id:int, course_id: int, current_user: User = Depends(get_current_user)):
    role_data = current_user['role']
    
    if role_data != 'admin' and role_data != 'teacher':
        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only admins and teachers can add users to courses.'
        )
    
    enroll_in_course(user_id, course_id)
    return f'User with user id: {user_id} added'


@enrollment_router.get('/courses/{email}')
def show_course(email:str, current_user: User = Depends(get_current_user)):
    email_data = current_user['email']
    
    if email != email_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user's information."
        )
    
    result = part_of_courses(email)
    
    return result