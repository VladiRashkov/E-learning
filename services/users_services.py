
from data.database import query
from fastapi import HTTPException, status



def all():
    data = query.table('users').select('*').execute()
    return data

def new_user(email:str, password:str):
    
    # if '@' not in username:
    #     return 'Please enter a valid email address!'
    data = query.table('users').select('*').eq('email', email).execute()
    
    if data == []:
        return None
    else:
        new_registration = query.table('users').insert({'email':email, 'password':password}).execute()
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