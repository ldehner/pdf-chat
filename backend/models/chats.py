from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    id: Optional[int]
    chat: Optional[int]
    question: str
    answer: Optional[str]

class Chat(BaseModel):
    id: Optional[int]
    owner: Optional[int]
    title: str
    last_updated: Optional[datetime]
    messages: Optional[list[Message]]