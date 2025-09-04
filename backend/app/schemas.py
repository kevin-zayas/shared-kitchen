from typing import List, Optional
from pydantic import BaseModel, EmailStr

# ====== USER SCHEMAS ======

class UserBase(BaseModel):
    username: str
    email: EmailStr

# Request model for creating a user
class UserCreate(UserBase):
    pass

# Response model for reading user data
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # tells Pydantic to convert SQLAlchemy objects to JSON


# ====== RECIPE SCHEMAS ======

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[str] = None  # kept as free-form strings for flexibility
    instructions: str
    owner_id: int

# Request model for creating a recipe
class RecipeCreate(RecipeBase):
    pass

# Response model for reading recipe data
class RecipeResponse(RecipeBase ):
    id: int

    class Config:
        orm_mode = True


# ====== RECIPE REVIEW SCHEMAS ======

class ReviewBase(BaseModel):
    rating: int  # could be 1–5 stars
    comment: Optional[str] = None
    recipe_id: int
    reviewer_id: int

# Request model for creating a recipe review
class ReviewCreate(ReviewBase):
    pass

# Response model for reading recipe review data
class ReviewResponse(ReviewBase):
    id: int

    class Config:
        orm_mode = True