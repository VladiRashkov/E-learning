from fastapi import APIRouter, Depends, Query, HTTPException, status
from FastAPI.services.courses_services import all, make_course
from FastAPI.data.models.user import User
from FastAPI.data.models.section import Section
from FastAPI.common.auth import get_current_user
from FastAPI.services.section_services import new_section, all_sections_under_course

section_router = APIRouter(prefix='/sections', tags=['sections'])



@section_router.post('/create')
def create_section(section:Section, current_user: User = Depends(get_current_user)):
    role = current_user['role']
    if role != 'teacher':
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail='Only teachers can create sections!'
            )
    result = new_section(section.course_id,section.content, section.description, section.external_resource_link)
    
    return result

@section_router.get('/')
def get_all(course_id:int):
    result = all_sections_under_course(course_id)
    return result


