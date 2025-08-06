from pydantic import BaseModel, EmailStr

# What we expect when creating a user
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# What we return when reading a user
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # tells Pydantic to convert SQLAlchemy objects to JSON