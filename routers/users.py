from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models import user

users_router = APIRouter(prefix='/users', tags = ['users'])


@users_router.get('/')
def get_users(sort: str| None = None):
    users = user_service.all()