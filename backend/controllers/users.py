from uuid import UUID
from fastapi import APIRouter, Path, HTTPException
from typing_extensions import Annotated
from models.users import UserModel
from logic import user_logic
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def get_users() -> list[UserModel]:
    pass

@router.post("/", status_code=201, response_model=UserModel)
async def create_user(user: UserModel) -> UserModel:
    print(user)
    try:
        return user_logic.register_user(user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Error occurred while creating user.")
    
@router.get("/{username}/{password}")
async def login_user(username: str, password: str) -> UserModel:
    try:
        return user_logic.login_user(username, password)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail="User unauthorized.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Error loggin in user.")

@router.delete("/{id}")
async def delete_user(id: Annotated[UUID, Path(ge=1)]):
    pass

@router.patch("/{id}")
async def update_user(id: Annotated[UUID, Path(ge=1)], user: UserModel) -> UserModel:
    pass