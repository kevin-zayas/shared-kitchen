from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency that creates a session and closes it after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/bulk", response_model=List[schemas.UserResponse])
def create_users_bulk(users: List[schemas.UserCreate] = Body(...), db: Session = Depends(get_db)):
    created_users = []
    for user in users:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            continue  # Skip already registered users
        new_user = models.User(username=user.username, email=user.email)
        db.add(new_user)
        created_users.append(new_user)
    db.commit()
    for user in created_users:
        db.refresh(user)
    return created_users
