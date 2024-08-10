from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWSError, jwt
from datetime import datetime, timedelta

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'
ACCESS_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer

token_blacklist = set()

def create_token(data: dict):
    expire = datetime.now() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    data.update({'exp': expire})
    
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    user_id = verify_access_token(token, credentials_exception)
    return int(user_id)

def logout_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token_blacklist.add(token.credentials)