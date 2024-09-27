import time
from fastapi import HTTPException
from sqlalchemy import DateTime
from repositories.message_repository import MessageRepository
from repositories.chat_repository import ChatRepository
from models.chats import ChatModel, MessageModel
from database.entities import ChatEntity, MessageEntity
from models.users import UserModel
from database.init_database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import uuid


def create_chat(chat: ChatModel) -> UserModel:
    db: Session = SessionLocal()
    try:
        repo = ChatRepository(db)
        entity = ChatEntity(
            id=uuid.uuid4(),
            title=chat.title,
            user_id=chat.user_id,
            last_updated=chat.last_updated,
            messages=chat.messages,
        )
        new_chat = repo.add(entity)
        return ChatModel(
            id=new_chat.id,
            title=new_chat.title,
            user_id=new_chat.user_id,
            last_updated=new_chat.last_updated,
            messages=new_chat.messages,
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()


def create_message(id: UUID, message: MessageModel) -> MessageModel:
    # TODO call answer logic here
    db: Session = SessionLocal()
    try:
        repo = MessageRepository(db)
        entity = MessageEntity(
            id=uuid.uuid4(),
            chat_id=id,
            answer="test",
            question=message.question,
            timestamp=message.timestamp,
        )
        new_message = repo.add(entity)
        time.sleep(2)
        return MessageModel(
            id=new_message.id,
            chat_id=new_message.chat_id,
            answer=new_message.answer,
            question=new_message.question,
            timestamp=new_message.timestamp,
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()
