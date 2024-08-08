from fastapi import APIRouter, Response, status, HTTPException, Header



student_router = APIRouter(prefix='/students', tags =['students'])


@student_router.get('/')