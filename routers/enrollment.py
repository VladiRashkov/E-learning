from fastapi import APIRouter, HTTPException, status
from services.enrollment_services import enroll_in_course, part_of_courses
from fastapi import Depends
from data.models.user import User
from common.auth import get_current_user
enrollment_router = APIRouter(prefix='/enroll', tags=['enrollment'])



# admin adds a user to premium to a specific course that the user will be able to access
# needs admin token verication
@enrollment_router.put('/add_user/{user_id}')
def add_user_to_course(user_id:int, course_id: int):
    result = enroll_in_course(user_id, course_id)
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