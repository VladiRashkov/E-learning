from data.database import query
from fastapi import HTTPException, status



def create(name:str):
    query.table('tags').insert({'name':name}).execute()
    
    return True