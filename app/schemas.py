from pydantic import BaseModel,HttpUrl, EmailStr
from datetime import datetime

class CourseCreate(BaseModel):
    name: str
    instructor: str
    address: str
    website: str


class CourseResponse(CourseCreate): 
    id: int

    class Config:
            orm_model = True


class UserCreate(BaseModel):
    
     email: EmailStr
     password: str


class UserRes(BaseModel):
     id: int
     email: EmailStr
     created_at: datetime

     class Config:
                 orm_model = True


# class UserLogIn(BaseModel):
#       email : EmailStr
#       password : str

      
     