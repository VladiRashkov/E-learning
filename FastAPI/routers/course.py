from fastapi import APIRouter, Depends, Query, HTTPException, status
from FastAPI.services.courses_services import all, make_course, request_to_participate, \
    update_course, discover_course, find_course_by_tag, rate_course, get_average_score
from FastAPI.data.models.user import User, UserRole
from FastAPI.data.models.course import CreateCourse, UpdateCourse
from FastAPI.common.auth import get_current_user
from fastapi_pagination import Page, add_pagination, paginate
from typing import Optional

course_router = APIRouter(prefix='/courses', tags=['courses'])

# view by anybody  response_model=Page[CreateCourse]
@course_router.get('/')
async def get_courses():
    courses = all()
    return courses


#token to be implemented
@course_router.post('/new_course')
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
                         create_course.objectives,
                         create_course.link_course)
    
    return result


@course_router.put('/update')
def modify(title: str, course_data: UpdateCourse, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Only teachers can create sections!'
        )

    existing_course = discover_course(title)

    updated_course_data = {
        "course_id":existing_course[0]["course_id"],
        "title": course_data.title if course_data.title else existing_course[0]["title"],
        "description": course_data.description if course_data.description else existing_course[0]["description"],
        "objectives": course_data.objectives if course_data.objectives else existing_course[0]["objectives"],
        "home_page_picture": course_data.home_page_picture if course_data.home_page_picture else existing_course[0]["home_page_picture"],
        "is_premium": course_data.is_premium if course_data.is_premium else existing_course[0]["is_premium"],
        "rating": course_data.rating if course_data.rating else existing_course[0]["rating"],
        "link_course": course_data.link_course if course_data.link_course else existing_course[0]["link_course"],
    }

    update_course(**updated_course_data)

    return {'message': 'Course data updated'}

@course_router.put('/join_course')
def participate(title: str, current_user: User = Depends(get_current_user)):
    user_id = current_user['user_id']  # Get user_id from the current user
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user data"
        )
    
    # Call the function to handle course participation
    request_to_participate(title, user_id)
    
    return {'message': f'The user has been added to the course {title}'}

    
@course_router.get('/tag')
def find_by_course(tag_name:str):
    result = find_course_by_tag(tag_name)
    return result


@course_router.put('/rate')
def rate(email:str, score:float, course_name: str, current_user: User = Depends(get_current_user)):
    if score > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The scode has to be between 0 and 10')
    email_logged_user = current_user['email']
    
    if email != email_logged_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not authorized')
    
    result = rate_course(email, score, course_name)
    
    return {"message": "Rating submitted successfully", "result": result}

@course_router.get('/average_score')
def average_score(score_id:int):
    result = get_average_score(score_id)
    return f'Course average score {result:.2f} coresult'


