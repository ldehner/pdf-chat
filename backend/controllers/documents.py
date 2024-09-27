from uuid import UUID

from fastapi import APIRouter, Path, UploadFile, File, BackgroundTasks, Response, status, Form
from starlette.responses import StreamingResponse
from typing_extensions import Annotated

from models.documents import ChatDocument
from services.documents import DocumentsService
from logic import documents_logic

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/")
async def get_documents() -> list[UploadFile]:
    pass

@router.post("/")
async def create_document(background_tasks: BackgroundTasks,
                          user_id: UUID = Form(...),
                          file: UploadFile = File(...)) -> Response:

    document = await DocumentsService.add_document(file, user_id)
    background_tasks.add_task(DocumentsService.generate_embeddings, document)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/documents/{document.id}"}
    )

@router.get("/{id}", responses={
    200: {
        "content": {"application/pdf": {}},
        "description": "Returns a PDF file"
    },
    404: {
        "description": "Document not found"
    }
})
async def get_document(id: UUID):
    doc = documents_logic.get_document(id)
    return StreamingResponse(
        iter([doc.content]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{doc.title}"'
        }
    )

@router.delete("/{id}")
async def delete_document(id: Annotated[int, Path(ge=1)]):
    pass