from fastapi import APIRouter, Depends, Query, HTTPException, status
from services.courses_services import all, make_course
from data.models.user import User
from data.models.section import Section
from common.auth import get_current_user
from services.section_services import new_section

section_router = APIRouter(prefix='/section', tags=['sections'])



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