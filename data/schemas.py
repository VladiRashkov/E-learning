from pydantic import BaseModel


class CreateCourse(BaseModel):
    title:str
    description:str
    home_page_picture:str
    is_premium:bool = False
    rating: float
    objectives:str
