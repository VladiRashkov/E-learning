from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models.user import LoginData, UpdateUserData
from services.users_services import all, new_user, completed_account
from fastapi.requests import Request
import re

users_router = APIRouter(prefix='/users', tags = ['users'])


@users_router.get('/')
def get_users(sort: str| None = None):
    users = all()
    return users    

@users_router.post('/new_account')
def create_user(user_reg:LoginData, response:Response):
    
    if '@' not in user_reg.email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Please enter a valid email address with an "@" symbol.'}
    
    pass_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not bool(re.match(pass_pattern,user_reg.password)):
        return {'message': 'Password must be at least 8 characters long, include upper and lower case letters, a number, and a special character.'}
    
    user = new_user(user_reg.email, user_reg.password)
    
    if user:
        return 'Registration completed!'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Username{user_reg.email} is taken!'}   

@users_router.put('/update_user/{email}')
def update_user(email:str, user_data:UpdateUserData, response:Response):
    completed_account(email=email,  
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        photo=user_data.photo,
        role=user_data.role,
        phone_number=user_data.phone_number,
        linkedin_account=user_data.linkedin_account
        )
    
    return f'User with email address {email} has completed their profile'