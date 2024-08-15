from fastapi import APIRouter
from services.courses_services import all, make_course
from data.models import course
from data.schemas import CreateCourse

course_router = APIRouter(prefix='/courses', tags=['courses'])


# view by anybody
@course_router.get('/')
def get_courses():
    courses = all()
    return courses





@course_router.post('new_course')
def create_new_course(create_course:CreateCourse):
    result = make_course(create_course.title,
                         create_course.description,
                         create_course.home_page_picture,
                         create_course.is_premium,
                         create_course.rating,
                         create_course.objectives)
    return result


# class CreateTransaction(BaseModel):
#     receiver_id: int
#     amount: float
#     category: str
