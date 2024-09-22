import pymupdf
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.documents import ChatDocument


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
    async def add_document(file: UploadFile) -> ChatDocument:
        doc = pymupdf.open(stream=file.file, filetype="pdf")
        title = file.filename

        # TODO: Add document to database. Id must be autogenerated and changed below
        return ChatDocument(id=1, title=title, content=doc.write())
