from fastapi import FastAPI
from app.routers import users, recipes

app = FastAPI()
app.include_router(users.router)
app.include_router(recipes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Shared Kitchen!"}