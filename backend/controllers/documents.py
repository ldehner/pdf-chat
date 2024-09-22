from fastapi import APIRouter, Path, UploadFile, File, BackgroundTasks, Response, status
from typing_extensions import Annotated
from services.documents import DocumentsService

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/")
async def get_documents() -> list[UploadFile]:
    pass

@router.post("/")
async def create_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> Response:
    document = await DocumentsService.add_document(file)
    background_tasks.add_task(DocumentsService.generate_embeddings, document)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/documents/{document.id}"}
    )

@router.get("/{id}")
async def get_document(id: Annotated[int, Path(ge=1)]):
    pass

@router.delete("/{id}")
async def delete_document(id: Annotated[int, Path(ge=1)]):
    pass