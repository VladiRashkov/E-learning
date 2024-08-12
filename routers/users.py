from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models.user import LoginData
from services.users_services import all, new_user
from fastapi.requests import Request



users_router = APIRouter(prefix='/users', tags = ['users'])


@users_router.get('/')
def get_users(sort: str| None = None):
    users = all()
    return users    

@users_router.post('/new_account')
def create_user(user_reg:LoginData, response:Response):
    user = new_user(user_reg.username, user_reg.password)
    
    if user:
        return 'Registration completed!'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Username{user_reg.username} is taken!'}   
