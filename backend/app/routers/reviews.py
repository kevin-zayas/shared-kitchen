from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new review
@router.post("/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Validate recipe exists
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == review.recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Validate user exists
    db_user = db.query(models.User).filter(models.User.id == review.reviewer_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Reviewer not found")

    new_review = models.Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Get all reviews for a specific recipe
@router.get("/recipe/{recipe_id}", response_model=List[schemas.ReviewResponse])
def get_reviews_for_recipe(recipe_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.recipe_id == recipe_id).all()
    return reviews  

#not sure if needed
# Get all reviews written by a specific user
@router.get("/user/{user_id}", response_model=List[schemas.ReviewResponse])
def get_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.reviewer_id == user_id).all()
    return reviews

# Delete a review
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}

# Update a review
@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, updated_review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Validate updating user is existing user
    if updated_review.reviewer_id != review.reviewer_id:
        raise HTTPException(status_code=400, detail="Not Original Reviewer")

    # Update fields
    review.rating = updated_review.rating
    review.comment = updated_review.comment
    # review.recipe_id = updated_review.recipe_id
    # review.reviewer_id = updated_review.reviewer_id

    db.commit()
    db.refresh(review)
    return review