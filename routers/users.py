from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models import user
from services.users_services import all
users_router = APIRouter(prefix='/users', tags = ['users'])


@users_router.get('/')
def get_users(sort: str| None = None):
    users = all()
    return users    