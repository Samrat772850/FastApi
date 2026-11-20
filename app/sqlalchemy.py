
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from . import models, schemas, utils 
from .database import engine, get_db
from typing import List


app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Pydantic Schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    address: str
    website: str



#Post - Create User
@app.post("/user", status_code=status.HTTP_201_CREATED,response_model=schemas.UserRes)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(400, "Email already exist")    
    hash_password = utils.hash_password(user.password)
    user.password = hash_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


# GET - Retrieve All Courses
@app.get("/alchemy", response_model= List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()

    return {
        "total": len(courses),
        "courses": courses
    }


# GET - Retrieve Course by ID
@app.get("/alchemy/{id}", response_model=schemas.CourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {id} not found"
        )

    return course


# PUT - Update Course
@app.put("/alchemy/{id}", response_model=schemas.CourseResponse)
def update_course(
    id: int,
    course:schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if db_course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id: {id} not found"
        )

    db_course.name = course.name
    db_course.instructor = course.instructor
    db_course.address = course.address
    db_course.website = str(course.website)

    db.commit()
    db.refresh(db_course)

    return db_course 


# DELETE - Delete Course
@app.delete("/alchemy/{id}")
def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {id} not found"
        )

    db.delete(course)
    db.commit()

    return {"message": "Course deleted successfully"}




