from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.types import UserDefinedType
import uuid

Base = declarative_base()

class PGVector(UserDefinedType):
    def get_col_spec(self):
        return "VECTOR(1536)"

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col

class UserEntity(Base):
    __tablename__ = 'user'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, nullable=False)
    
    chats = relationship("ChatEntity", back_populates="user")
    documents = relationship("DocumentEntity", back_populates="user")


class DocumentEntity(Base):
    __tablename__ = 'document'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    content = Column(LargeBinary, nullable=False)

    user = relationship("UserEntity", back_populates="documents")
    embeddings = relationship("EmbeddingEntity", back_populates="document")


class EmbeddingEntity(Base):
    __tablename__ = 'embedding'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pdf_id = Column(PG_UUID(as_uuid=True), ForeignKey('document.id'), nullable=False)
    vector = Column(PGVector, nullable=False)
    
    document = relationship("DocumentEntity", back_populates="embeddings")


class ChatEntity(Base):
    __tablename__ = 'chat'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    title = Column(String, nullable=False)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("UserEntity", back_populates="chats")
    messages = relationship("MessageEntity", back_populates="chat")


class MessageEntity(Base):
    __tablename__ = 'message'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    chat_id = Column(PG_UUID(as_uuid=True), ForeignKey('chat.id'), nullable=False)
    
    chat = relationship("ChatEntity", back_populates="messages")


def init_db(engine):
    Base.metadata.create_all(engine)