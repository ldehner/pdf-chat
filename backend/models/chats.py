from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class MessageModel(BaseModel):
    id: Optional[UUID4]
    timestamp: datetime
    question: str
    answer: Optional[str]
    chat_id: UUID4

    class Config:
        from_attributes = True

class ChatModel(BaseModel):
    id: Optional[UUID4]
    user_id: UUID4
    title: str
    last_updated: Optional[datetime]
    messages: Optional[List[MessageModel]]

    class Config:
        from_attributes = True