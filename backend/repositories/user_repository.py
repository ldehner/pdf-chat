from database.entities import UserEntity
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)
    
    def get_by_name(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.name == username).first()
