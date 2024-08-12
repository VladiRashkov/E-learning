from data.database import query
from fastapi import HTTPException, status



def all():
    data = query.table('users').select('*').execute()
    return data

def new_user(username:str, password:str):
    data = query.table('users').select('*').eq('email', username).execute()
    
    if data == []:
        return None
    else:
        new_registration = query.table('users').insert({'email':username, 'password':password}).execute()
        return new_registration