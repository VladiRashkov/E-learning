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