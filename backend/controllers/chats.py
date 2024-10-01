from fastapi import APIRouter, HTTPException, Path
from pydantic import UUID4
from typing_extensions import Annotated
from logic import chat_logic
from sqlalchemy.exc import SQLAlchemyError
from models.chats import ChatModel, MessageModel

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/")
async def get_chats() -> list[ChatModel]:
    pass


@router.post("/")
async def create_chat(chat: ChatModel) -> ChatModel:
    print(chat)
    try:
        return chat_logic.create_chat(chat)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400, detail="Error occurred while creating chat."
        )


@router.get("/{id}")
async def get_chat(id: Annotated[int, Path(ge=1)]) -> ChatModel:
    pass


@router.delete("/{id}")
async def delete_chat(id: Annotated[int, Path(ge=1)]):
    pass


@router.patch("/{id}")
async def update_chat(id: Annotated[int, Path(ge=1)], chat: ChatModel) -> ChatModel:
    pass


@router.get("/{id}/messages")
async def get_messages(id: Annotated[int, Path(ge=1)]) -> list[MessageModel]:
    pass


@router.post("/{id}/messages")
async def create_message(id: UUID4, message: MessageModel) -> MessageModel:
    print(message)
    try:
        return chat_logic.create_message(id, message)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400, detail="Error occurred while creating chat."
        )
