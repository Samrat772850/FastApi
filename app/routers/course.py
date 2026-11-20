from fastapi import FastAPI, HTTPException, Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db
from typing import List

router = APIRouter(
    prefix="/alchemy",
    tags=["alchemy"]
)




# POST - Create Course
@router.post("/", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    
    
    new_details = models.Course(**course.model_dump())
    new_details.website=str(course.website)
    

    db.add(new_details)
    db.commit()
    db.refresh(new_details)

    return new_details



# GET - Retrieve All Courses
@router.get("/", response_model= List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()

    return courses


# GET - Retrieve Course by ID
@router.get("/{id}", response_model=schemas.CourseResponse)
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
@router.put("/{id}", response_model=schemas.CourseResponse)
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
@router.delete("/{id}")
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
