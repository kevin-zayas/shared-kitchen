from fastapi import APIRouter

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.get("/")
def get_recipes():
    return [{"id": 1, "title": "Banana Bread"}, {"id": 2, "title": "Tacos"}]