from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    customer="customer"
    admin="admin"

class User(BaseModel):
    id: Optional[int]
    username: str
    role: str