from fastapi import APIRouter
from services.enrollment_services import enroll_in_course

enrollment_router = APIRouter(prefix='/enroll', tags=['enrollment'])



# admin adds a user to premium to a specific course that the user will be able to access
# needs admin token verication
@enrollment_router.put('/add_user/{user_id}')
def add_user_to_course(user_id:int, course_id: int):
    result = enroll_in_course(user_id, course_id)
    return f'User with user id: {user_id} added'