from data.database import query
from fastapi import HTTPException, status


def new_section(course_id:int,title:str, content:str, description:str, external_resource_link:str):
    query.table('sections').insert({
        'course_id':course_id,
        'title': title,
        'content': content,
        'description': description,  # Corrected the typo here
        'external_resource_link': external_resource_link
    }).execute()
    
    
    return True