from repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class MessageRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)
