
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


# POST - Create User
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRes
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hashed_password = utils.hash_password(user.password)

    new_user = models.User(
        
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET - Retrieve All Users
@router.get(
    "/",
    response_model=List[schemas.UserRes]
)
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


# GET - Retrieve User by ID
@router.get(
    "/{id}",
    response_model=schemas.UserRes
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    return user


# PUT - Update User
@router.put(
    "/{id}",
    response_model=schemas.UserRes
)
def update_user(
    id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    existing_email = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.id != id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
  
    db_user.email = user.email
    db_user.password = utils.hash_password(user.password)

    db.commit()
    db.refresh(db_user)

    return db_user


# DELETE - Delete User
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    db.delete(user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
