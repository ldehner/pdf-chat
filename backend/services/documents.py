from uuid import UUID

import pymupdf
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.documents import ChatDocument
from logic import documents_logic

class DocumentsService:

    @staticmethod
    async def generate_embeddings(doc: ChatDocument):
        content = pymupdf.open(stream=doc.content, filetype="pdf")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        documents = []

        for page in content.pages():
            documents.append(
                Document(
                    page_content= page.get_text(),
                    metadata={
                        "id": doc.id,
                        "page_number": page.page_number
                    }
                )
            )

        split_documents = text_splitter.split_documents(documents)
        #TODO: Calculate embeddings and add them to Vectorstore


    @staticmethod
    async def add_document(file: UploadFile, user_id: UUID) -> ChatDocument:
        content = await file.read()
        title = file.filename

        chat_document = ChatDocument(title=title, content=content, owner=user_id)
        return documents_logic.save_document(chat_document)
