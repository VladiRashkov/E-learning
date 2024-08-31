from data.database import query
from fastapi import HTTPException, status
import bcrypt


def all():
    data = query.table('users').select('*').execute()
    
    return data


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    
    return hashed_password.decode('utf-8')


def new_user(email:str, password:str):
    data = query.table('users').select('*').eq('email', email).execute()
    hashed_password = hash_password(password)
    
    if data == []:
        return None
    else:
        new_registration = query.table('users').insert({'email':email, 'password':hashed_password}).execute()
        return new_registration
    
    
def completed_account(email:str, first_name:str, last_name:str, photo:str, role:str, phone_number:str, linkedin_account:str):
    find_user = query.table('users').select('*').eq('email',email).execute()
    
    if not find_user:
        return None
    else:
        details_user = query.table('users').update({'first_name':first_name, 'last_name':last_name, 
                                                    'photo':photo, 
                                                    'role':role, 
                                                    'phone_number':phone_number, 
                                                    'linkedin_account':linkedin_account}).eq('email', email).execute()
    
        return details_user
    
    
def get_user_by_id(user_id:int):
    result = query.table('users').select('*').eq('user_id',user_id).execute()
    return result


def verify_user_credentials(email: str, password: str):
    try:
        user = query.table('users').select('*').eq('email', email).execute()
        user_list = user.data
        if not user_list:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        user = user_list[0]

        
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
def remove_from_course(email:str, title:str):
    user = query.table('users').select('*').eq('email',email).execute()
    student_id = user.data[0]['user_id']
    
    # course_involvment = query.table('enrollment').select('*').eq('student_id',student_id).execute()
    # course_id = course_involvment.data[1]
    course = query.table('courses').select('course_id').eq('title',title).execute()
    course_id = course.data[0]['course_id']
    query.table('enrollments').update({'is_subscribed': False}).eq('student_id', student_id).eq('course_id', course_id).execute()


    # query.table('enrollment').update({'student_id':student_id, 'course_id':course_id, 'is_subscribed':False}).eq('course_id',course_id).execute()
    
    return True
    
def changing_password(email:str, password:str):
    user = query.table('users').select('*').eq('email',email).execute()
    
    hashed_password = hash_password(password)
    if user == []:
        return None
    else:
        query.table('users').update({'password':hashed_password}).eq('email', email).execute()
        return True
        
def discover_user(email: str):
    response = query.table('users').select('*').eq('email', email).execute()
    
    # Check if the response contains data
    if not response or not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Assuming the response has a 'data' attribute that contains the list of users
    existing_user = response.data
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Assuming existing_user is a list, and you want to access the first user's email
    return existing_user
    