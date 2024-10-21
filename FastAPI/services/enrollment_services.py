from FastAPI.data.database import query
from fastapi import HTTPException, status


#admin or teacher confirmation to be implemented
def enroll_in_course(user_id:int, course_id:int):
    user_to_be_enrolled = query.table('users').select('*').eq('user_id',user_id).execute()
    user_list = user_to_be_enrolled.data
    id = user_list[0]['user_id']
    
    result = query.table('enrollments').insert({'student_id':id, 'course_id':course_id, 'is_subscribed': True}).execute()
    return result


def part_of_courses(email: str):
    # Fetch all non-premium courses
    all_public_data = query.table('courses').select('*').eq('is_premium', False).execute()
    all_courses = all_public_data.data
    
    # Fetch user details using email
    user_result = query.table('users').select('user_id').eq('email', email).execute()
    
    if user_result.data:
        user = user_result.data[0]  # Access the first user object
        student_id = user['user_id']
        
        # Fetch enrollments for the student
        enrolled_result = query.table('enrollments').select('course_id').eq('student_id', student_id).execute()
        
        if enrolled_result.data:
            course_ids = [enrollment['course_id'] for enrollment in enrolled_result.data]
            
            # Fetch subscribed enrollments
            subscribed_result = query.table('enrollments') \
                .select('course_id') \
                .eq('student_id', student_id) \
                .in_('course_id', course_ids) \
                .eq('is_subscribed', True) \
                .execute()
            
            if subscribed_result.data:
                subscribed_course_ids = [sub['course_id'] for sub in subscribed_result.data]
                
                # Fetch course data for subscribed courses that are premium
                sub_courses_user = query.table('courses') \
                    .select('*') \
                    .in_('course_id', subscribed_course_ids) \
                    .eq('is_premium', True) \
                    .execute()
                
                subscribed_courses_data = sub_courses_user.data
                
                return all_courses, subscribed_courses_data
            else:
                return all_courses, []  # No subscribed courses found
        else:
            return all_courses, []  # No enrolled courses found
    else:
        raise ValueError("No user found with the provided email.")
