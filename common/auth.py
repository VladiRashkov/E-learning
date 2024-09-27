from fastapi import Depends, status, HTTPException, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from services.users_services import get_user_by_id
from pydantic import BaseModel
import bcrypt

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'
ACCESS_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer()

token_blacklist = set()

class TokenData(BaseModel):
    user_id: int

def create_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: HTTPAuthorizationCredentials, credentials_exception):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        
        if user_id is None or token.credentials in token_blacklist:
            raise credentials_exception
        return user_id

    except JWTError:
        raise credentials_exception

def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(token, credentials_exception)
    user_response = get_user_by_id(user_id)

    if not user_response.data or len(user_response.data) == 0:
        raise credentials_exception

    
    user = user_response.data[0]

    return user

def logout_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token_blacklist.add(token.credentials)
    return {"message": "User successfully logged out"}




    