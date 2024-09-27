from pydantic import BaseModel, UUID4
from typing import Optional, List


class EmbeddingModel(BaseModel):
    id: Optional[UUID4]
    pdf_id: UUID4
    vector: List[float]

    class Config:
        from_attributes = True

class DocumentModel(BaseModel):
    id: Optional[UUID4]
    name: str
    user_id: UUID4
    embeddings: Optional[List[EmbeddingModel]]

    class Config:
        from_attributes = True

class ChatDocument(BaseModel):
    id: Optional[UUID4] = None
    title: str
    content: bytes
    owner: UUID4