from fastapi import APIRouter, Path
from typing_extensions import Annotated

from models.chats import ChatModel, MessageModel

router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

@router.get("/")
async def get_chats() -> list[ChatModel]:
    pass

@router.post("/")
async def create_chat(chat: ChatModel) -> ChatModel:
    pass

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
async def create_message(id: Annotated[int, Path(ge=1)], message: MessageModel) -> MessageModel:
    pass