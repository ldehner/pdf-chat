from pydantic import BaseModel, UUID4
from typing import Optional, List

from models.chats import ChatModel

class UserModel(BaseModel):
    id: Optional[UUID4] = None
    name: str
    isAdmin: bool
    chats: Optional[List[ChatModel]] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True