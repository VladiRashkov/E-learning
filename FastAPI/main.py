from routers.users import users_router
from routers.course import course_router
from routers.enrollment import enrollment_router
from routers.admin import admin_router
from routers.section import section_router
from fastapi import FastAPI


app = FastAPI()


app.include_router(users_router)
app.include_router(admin_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(section_router)