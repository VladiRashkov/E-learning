from data.database import query
from fastapi import HTTPException, status


#admin or teacher confirmation to be implemented
def enroll_in_course(user_id:int, course_id:int):
    user_to_be_enrolled = query.table('users').select('*').eq('user_id',user_id).execute()
    user_list = user_to_be_enrolled.data
    id = user_list[0]['user_id']
    
    result = query.table('enrollments').insert({'student_id':id, 'course_id':course_id, 'is_subscribed': True}).execute()
    return result


def part_of_courses(email:str):
    all_public = query.table('courses').select('*').eq('is_premium', False).execute()
    
    user = query.table('users').select('*').eq('email', email).execute()
    
    student_id = user[0]['student_id']
    
    enrolled = query.table('enrollments').select('*').eq('student_id', student_id).execute()
    
    courses_enrolled = enrolled[0]['course_id']
    
    subscribed = query.table('enrollments').select('*').eq('student_id',student_id, 'course_id', courses_enrolled ,'is_subscibed', True).execute()
    
    return all_public, subscribed