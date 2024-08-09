from routers.users import users_router
from fastapi import FastAPI


app = FastAPI()


app.include_router(users_router)