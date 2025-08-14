from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from typing import List
from app.database import SessionLocal

router = APIRouter(
    prefix="/follows",
    tags=["Follows"]
)

# Dependency that creates a session and closes it after the request
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Follow a user
@router.post("/{following_id}")
def follow_user(following_id: int, db: Session = Depends(get_db), current_user_id: int = 1):
    """
    current_user_id is temporary; later this comes from authentication
    """
    # Check if following user exists
    target_user = db.query(models.User).filter(models.User.id == following_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already following
    existing = db.query(models.Follow).filter_by(
        follower_id=current_user_id, following_id=following_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    follow = models.Follow(follower_id=current_user_id, following_id=following_id)
    db.add(follow)
    db.commit()
    return {"message": f"Now following user {following_id}"}

# Get list of users you follow
@router.get("/", response_model=List[int])
def get_following(db: Session = Depends(get_db), current_user_id: int = 1):
    follows = db.query(models.Follow).filter(models.Follow.follower_id == current_user_id).all()
    return [f.following_id for f in follows]

# Unfollow a user
@router.delete("/{following_id}")
def unfollow_user(following_id: int, db: Session = Depends(get_db), current_user_id: int = 1):
    """
    Remove a follow relationship. current_user_id is temporary; replace with auth later.
    """
    follow = db.query(models.Follow).filter_by(
        follower_id=current_user_id, following_id=following_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    db.delete(follow)
    db.commit()
    return {"message": f"Unfollowed user {following_id}"}