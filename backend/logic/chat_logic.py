import time
from fastapi import HTTPException
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import DateTime
from repositories.message_repository import MessageRepository
from repositories.chat_repository import ChatRepository
from models.chats import ChatModel, MessageModel
from database.entities import ChatEntity, MessageEntity
from models.users import UserModel
from database.init_database import SessionLocal, DATABASE_URL
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import uuid
from services.response import get_response
from datetime import datetime


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
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = PGVector(
        embeddings=embeddings,
        connection=DATABASE_URL,
        collection_name="docs_embeddings",
        use_jsonb=True
    )
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    retrieved_docs = retriever.invoke(message.question)
    content = []
    for doc in retrieved_docs:
        content.append(doc.page_content)

    response = get_response(message.question, content)
    db: Session = SessionLocal()
    try:
        repo = MessageRepository(db)
        entity = MessageEntity(
            id=uuid.uuid4(),
            chat_id=id,
            answer=response,
            question=message.question,
            timestamp=datetime.now(),
        )
        new_message = repo.add(entity)
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
