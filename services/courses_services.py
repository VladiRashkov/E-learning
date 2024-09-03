from data.database import query
from fastapi import HTTPException, status

def all():
    data = query.table('courses').select('*').execute()
    return data


def make_course(title:str, description:str, home_page_picture:str, is_premium:bool, rating:float, objectives:str):
    insert_course = query.table('cours  es').insert({'title': title, 'description':description, 
                                   'home_page_picture':home_page_picture, 'is_premium':is_premium,
                                   'rating':rating, 'objectives': objectives}).execute()
    return insert_course


def request_to_participate(title:str, user_id: int):
    course_details = query.table('courses').select('*').eq('title',title).execute()
    course_id = course_details.data[0]['course_id']
    
    result = query.table('enrollments').insert({'student_id':user_id, 'course_id':course_id, 'is_subscribed': True}).execute()
    return True


def update_course(course_id:int, title: str, description: str, home_page_picture: str, is_premium: bool, rating: float, objectives: str):
    result = query.table('courses').select('*').eq('course_id', course_id).execute()

    if result==[]:
        return None
    else:
        details_course = query.table('courses').update({
            'title': title,
            'description': description,
            'objectives': objectives,
            'home_page_picture': home_page_picture,
            'is_premium': is_premium,
            'rating': rating,
        }).eq('course_id', course_id).execute()

        return details_course
    
    
def discover_course(title:str):
    result = query.table('courses').select('*').eq('title',title).execute()
    
    if not result or not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )
    existing_course = result.data

    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found."
        )
        
        
    return existing_course


def find_course_by_tag(name:str):
    tag_data = query.table('tags').select('*').eq('name',name).execute()
    tag_data_list = tag_data.data
    
    if not tag_data_list:
        return {"error": "Tag not found"}
    
    tag_id = tag_data_list[0]['tag_id']
    coursetags_data = query.table('coursetags').select('*').eq('tag_id', tag_id).execute()
    coursetags_data_list = coursetags_data.data
    
    if not coursetags_data_list:
        return {"error": "No courses found for this tag"}
    
    course_id = coursetags_data_list[0]['course_id']
    
    # Fetching the actual course data using course_id
    course_data = query.table('courses').select('*').eq('course_id', course_id).execute()
    course_data_list = course_data.data
    
    return course_data_list