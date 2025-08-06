from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users():
    return [{"id": 1, "username": "alice"}, {"id": 2, "username": "bob"}]