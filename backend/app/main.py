from fastapi import FastAPI
from app.routers import users, recipes
from app.database import engine, Base


app = FastAPI()
app.include_router(users.router)
app.include_router(recipes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Shared Kitchen!"}

# Creates tables based on your model definitions
Base.metadata.create_all(bind=engine)