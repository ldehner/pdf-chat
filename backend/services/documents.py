from uuid import UUID

import pymupdf
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.documents import ChatDocument
from logic import documents_logic
from database.init_database import DATABASE_URL
from langchain_ollama import OllamaEmbeddings


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
                    page_content=page.get_text(),
                    metadata={"id": str(doc.id), "page_number": page.number},
                )
            )

        split_documents = text_splitter.split_documents(documents)
        embeddings = OllamaEmbeddings(model="wizardlm2:7b", base_url="ollama:11434")
        vector_store = PGVector(
            embeddings=embeddings,
            connection=DATABASE_URL,
            collection_name="docs_embeddings",
            use_jsonb=True,
        )
        vector_store.add_documents(split_documents)

    @staticmethod
    async def add_document(file: UploadFile, user_id: UUID) -> ChatDocument:
        content = await file.read()
        title = file.filename

        chat_document = ChatDocument(title=title, content=content, owner=user_id)
        return documents_logic.save_document(chat_document)
