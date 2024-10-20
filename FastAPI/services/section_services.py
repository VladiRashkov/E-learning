from FastAPI.data.database import query
from fastapi import HTTPException, status


def new_section(course_id:int,title:str, content:str, description:str, external_resource_link:str):
    query.table('sections').insert({
        'course_id':course_id,
        'title': title,
        'content': content,
        'description': description,  # Corrected the typo here
        'external_resource_link': external_resource_link
    }).eq().execute()
    
    return True


def all_sections_under_course(course_id:int):
    
    result =  query.table('sections').select('*').eq('course_id',course_id).execute()
    
    return result