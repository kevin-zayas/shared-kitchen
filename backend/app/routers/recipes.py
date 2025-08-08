from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

# Dependency that creates a session and closes it after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RecipeRead)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == recipe.owner_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Recipe owner not found")

    new_recipe = models.Recipe(**recipe.model_dump())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.post("/bulk", response_model=List[schemas.RecipeRead])
def create_recipes_bulk(recipes: List[schemas.RecipeCreate] = Body(...), db: Session = Depends(get_db)):
    db_recipes = []

    for recipe in recipes:
        try:
            db_user = db.query(models.User).filter(models.User.id == recipe.owner_id).first()
            if not db_user:
                continue  # Skip if owner not found

            new_recipe = models.Recipe(**recipe.model_dump())
            db.add(new_recipe)
            db_recipes.append(new_recipe)

        except Exception:
            continue  # Skip if any error occurs

    db.commit()

    for recipe in db_recipes:
        db.refresh(recipe)

    return db_recipes

@router.get("/", response_model=List[schemas.RecipeRead])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()
