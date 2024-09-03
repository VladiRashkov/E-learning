
from fastapi import APIRouter, Depends,HTTPException, status
from data.models.tags import Tag
from data.models.user import User
from common.auth import get_current_user
from services.tag_services import create


tags_router = APIRouter(prefix='/tags', tags = ['tags'])

@tags_router.post('/new')
def create_tag(name:str, user_data:User, current_user = Depends(get_current_user)):
    
    # email_data = current_user['email']
    
    # if email != email_data:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You are not authorized to update this user's information."
    #     )
    
    if user_data.role:
        role = user_data.role.lower()
        
        if role !='teacher' or role !='admin':
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user's information."
        )
        
    create(name)
    
    return {'message':'Tag created'}
    
    
    