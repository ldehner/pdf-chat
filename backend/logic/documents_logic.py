import json
import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.entities import DocumentEntity
from database.init_database import SessionLocal
from models.documents import ChatDocument
from repositories.document_repository import DocumentRepository


def save_document(doc: ChatDocument) -> ChatDocument:
    db: Session = SessionLocal()
    try:
        repo = DocumentRepository(db)
        entity = DocumentEntity(id=uuid.uuid4(), title=doc.title, content=doc.content, user_id=doc.owner)
        new_entity = repo.add(entity)
        return ChatDocument(id=new_entity.id,
                            title=new_entity.title,
                            content=new_entity.content,
                            owner=new_entity.user_id)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()

def get_document(id: uuid.UUID) -> ChatDocument:
    db: Session = SessionLocal()
    try:
        repo = DocumentRepository(db)
        entity = repo.get_by_id(DocumentEntity,id)
        return ChatDocument(id=entity.id,
                        title=entity.title,
                        content=entity.content,
                        owner=entity.user_id)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()