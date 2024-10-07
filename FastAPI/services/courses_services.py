from data.database import query
from fastapi import HTTPException, status
from functools import reduce
from data.models.course import CreateCourse

def all():
    data = query.table('courses').select('*').execute()
    
    courses = [
        CreateCourse(
            title=row['title'],
            description=row['description'],
            home_page_picture=row['home_page_picture'],
            is_premium = row['is_premium'],
            rating= row['rating'],
            objectives=row['objectives']
        )
        for row in data.data
    ]
    
    return courses
        
    #  users = [
    #     User(
    #         id=row['user_id'],  # Assuming 'user_id' is the key in the dictionary
    #         email=row['email'],
    #         first_name=row['first_name'],
    #         last_name=row['last_name'],
    #         password=row['password'],
    #         photo=row['photo'],
    #         role=row['role'],
    #         phone_number=row['phone_number'],
    #         linkedin_account=row['linkedin_account']
    #     )
    #     for row in data.data
    # ]
    # return users
  


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

#the course can be rated only if the user is enrolled in it - subscribed to the course
def rate_course(email: str, score: float, course_name: str):
    # Check if the user exists
    user_details = query.table('users').select('*').eq('email', email).execute()
    student_id = user_details.data[0]['user_id']
    
    # Check if the course exists
    course_details = query.table('courses').select('*').eq('title', course_name).execute()
    course_id = course_details.data[0]['course_id']
    
    # Check if the user is enrolled
    enrollment_data = query.table('enrollments').select('*')\
        .eq('student_id', student_id)\
        .eq('course_id', course_id)\
        .eq('is_subscribed', True).execute()
    
    if not enrollment_data.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not enrolled in the course')
    
    # Insert the rating
    rating_result = query.table('ratings').insert({'student_id': student_id,
                                                   'course_id': course_id, 'score': score}).execute()
    
    return {"rating_id": rating_result.data[0]['rating_id'], "score": score}
    
    
def get_average_score(course_id:int):
    list_data = query.table('ratings').select('*').eq('course_id',course_id).execute()
    
    if list_data==[]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No review have been added to this course yet!')
        
    list_scores = [item['score'] for item in list_data.data]
    len_list =len(list_scores)
    average_score = reduce(lambda x,y: x+y, list_scores)/len_list
    
    return average_score