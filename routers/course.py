from fastapi import APIRouter, Depends, Query, HTTPException, status
from services.courses_services import all, make_course
from data.models.user import User, UserRole
from data.schemas import CreateCourse
from common.auth import get_current_user

course_router = APIRouter(prefix='/courses', tags=['courses'])


# view by anybody
@course_router.get('/')
def get_courses():
    courses = all()
    return courses

#token to be implemented
@course_router.post('new_course')
def create_new_course(create_course:CreateCourse, current_user:User = Depends(get_current_user)):
    if not current_user.data or not isinstance(current_user.data, list) or len(current_user.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user data"
        )
    
    user_data = current_user.data[0]
    

    user_role = user_data.get('role')
    if user_role is None or user_role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a course"
        )
    
    
    result = make_course(create_course.title,
                         create_course.description,
                         create_course.home_page_picture,
                         create_course.is_premium,
                         create_course.rating,
                         create_course.objectives)
    return result

@course_router.put('/join_course')
def participate(title:str, current_user: User = Depends(get_current_user)):
    if not current_user.data or not isinstance(current_user.data, list) or len(current_user.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user data"
        )
    
