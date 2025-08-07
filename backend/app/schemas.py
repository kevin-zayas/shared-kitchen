from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Request model for creating a user
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# Response model for reading user data
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # tells Pydantic to convert SQLAlchemy objects to JSON

# Request model for creating a recipe
class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[str] = None
    instructions: str
    owner_id: int

# Response model for reading recipe data
class RecipeRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    ingredients: List[str] = None
    instructions: str
    owner_id: int

    class Config:
        orm_mode = True