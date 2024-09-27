from fastapi import HTTPException
from database.entities import UserEntity
from models.users import UserModel
from repositories import UserRepository
from database.init_database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import uuid


def register_user(user: UserModel) -> UserModel:
    db: Session = SessionLocal()
    try:
        repo = UserRepository(db)
        existing_users = repo.get_all(UserEntity)
        if len(existing_users) == 0:
            user.isAdmin = True
        entity = UserEntity(
            id=uuid.uuid4(),
            name=user.name,
            password=user.password,
            isAdmin=user.isAdmin,
        )
        new_user = repo.add(entity)
        return UserModel(id=new_user.id, name=new_user.name, isAdmin=new_user.isAdmin)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()


def login_user(username: str, password: str) -> UserModel:
    db: Session = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_by_name(username)

        if user is not None and user.password == password:
            return UserModel(
                id=user.id, name=user.name, isAdmin=user.isAdmin, chats=user.chats
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid password.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()
