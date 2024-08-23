from data.database import query

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