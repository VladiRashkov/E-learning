from data.database import query
from fastapi import HTTPException, status



def all():
    data = query.table('users').select('*').execute()
    return data