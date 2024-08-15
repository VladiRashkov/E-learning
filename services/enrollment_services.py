from data.database import query
from fastapi import HTTPException, status



def enroll_in_course(user_id:int, course_id:int):
    user_to_be_enrolled = query.table('users').select('*').eq('user_id',user_id).execute()
    user_list = user_to_be_enrolled.data
    id = user_list[0]['user_id']
    
    result = query.table('enrollments').insert({'student_id':id, 'course_id':course_id, 'is_subscribed': True}).execute()
    return result