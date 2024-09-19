from fastapi import APIRouter, Path
from typing_extensions import Annotated

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/")
async def get_documents():
    pass

@router.post("/")
async def create_document():
    pass

@router.get("/{id}")
async def get_document(id: Annotated[int, Path(ge=1)]):
    pass

@router.delete("/{id}")
async def delete_document(id: Annotated[int, Path(ge=1)]):
    pass