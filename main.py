from routers.users import users_router
from routers.course import course_router
from fastapi import FastAPI


app = FastAPI()


app.include_router(users_router)
app.include_router(course_router)