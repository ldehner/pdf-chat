from fastapi import APIRouter, Path
from typing_extensions import Annotated

from models.users import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def get_users() -> list[User]:
    pass

@router.post("/")
async def create_user(user: User) -> User:
    pass

@router.get("/{id}")
async def get_user(id: Annotated[int, Path(ge=1)]) -> User:
    pass

@router.delete("/{id}")
async def delete_user(id: Annotated[int, Path(ge=1)]):
    pass

@router.patch("/{id}")
async def update_user(id: Annotated[int, Path(ge=1)], user: User) -> User:
    pass