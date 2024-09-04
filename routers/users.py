from fastapi import APIRouter, Response, status, HTTPException, Header, Depends
from data.models.user import LoginData, UpdateUserData, User
from services.users_services import all, new_user, \
completed_account, get_user_by_id, verify_user_credentials, \
remove_from_course, changing_password, discover_user
from services.admin_services import save_role_change_request
from fastapi.requests import Request
import re
from common.auth import create_token, get_current_user, verify_access_token, logout_user, bearer_scheme
from fastapi.security import HTTPAuthorizationCredentials
from typing import Optional
from data.schemas import ChangePassword

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

    user_id = user.data[0]['user_id']
    token = create_token(user_id)
    
    
    if user:
        return 'Registration completed!', {"access_token": token, "token_type": "bearer"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Username{user_reg.email} is taken!'}   

@users_router.put('/update_user/{email}')
def update_user(email:str, user_data:UpdateUserData, response:Response, current_user:User = Depends(get_current_user)):
    email_data = current_user['email']
    
    if email != email_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user's information."
        )
        
    
    if user_data.role:
        role = user_data.role.lower()
            
        if role == 'teacher':
            completed_account(email=email,  
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            photo=user_data.photo,
            role=None,
            phone_number=user_data.phone_number,
            linkedin_account=user_data.linkedin_account
            )
    
            save_role_change_request(email=email, requested_role=role)
            return{
                'message':'Role "teacher" requires admin authorization. Your request has been submitted.'
            }
    
    completed_account(email=email,  
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        photo=user_data.photo,
        role=user_data.role,
        phone_number=user_data.phone_number,
        linkedin_account=user_data.linkedin_account
        )
    
    
    
    return f'User with email address {email} has completed their profile'


@users_router.post('/login')
def login(data: LoginData, response: Response):
    user = verify_user_credentials(data.email, data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = user['user_id']
    token = create_token(user_id)
    return {"access_token": token, "token_type": "bearer"}
# erase the token. It can be done only with java script
@users_router.post('/logout')
def logout(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return logout_user(token)

@users_router.put('/unsubscribe')
def unsubscribe_course(email:str, title:str, current_user:User = Depends(get_current_user)):
    
    email_data = current_user['email']
    
    if email != email_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user's information."
        )
        
    remove_from_course(email, title)
    return f'User removed from {title}!'



@users_router.put('/update_existing_user')
def modify(email:str, user_data:UpdateUserData, change_password:ChangePassword = None, current_user:User = Depends(get_current_user)):
    email_data = current_user['email']
    # limit this to teachers and students, the admin can only change his password
    role_data = current_user['role']
    
    if role_data == 'admin':
        return 'As an admin you can change only '
    
    if email != email_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user's information."
        )
    
    existing_user = discover_user(email)
    
    updated_user_data = {
    "email": email,
    "first_name": user_data.first_name if user_data.first_name else existing_user[0]["first_name"],
    "last_name": user_data.last_name if user_data.last_name else existing_user[0]["last_name"],
    "photo": user_data.photo if user_data.photo else existing_user[0]["photo"],
    "role": user_data.role if user_data.role else existing_user[0]["role"],
    "phone_number": user_data.phone_number if user_data.phone_number else existing_user[0]["phone_number"],
    "linkedin_account": user_data.linkedin_account if user_data.linkedin_account else existing_user[0]["linkedin_account"],
}
        
    completed_account(**updated_user_data)
    
    password = change_password.password
    
    if password == 'string':
        return {'message': 'Data updated'}
    pass_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not bool(re.match(pass_pattern,password)):
        return {'message': 'Password must be at least 8 characters long, include upper and lower case letters, a number, and a special character.'}
    changing_password(email,password)
    
    return {'message': 'Password changed. Data updated'}
    
    