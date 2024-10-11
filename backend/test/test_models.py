from typing import List

import pandas as pd
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymupdf import pymupdf
from tqdm import tqdm

TEST_DATABASE_URL = "postgresql://pdf_chat_user:5uperSecr3tP%40ssw0rd!@postgres:5432/pdf_chat_test"
PROMPT = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {contexts} 
    Answer:
    """

def get_response(question: str, text_segments: List[str], model) -> str:

    formatted_segments = "\n".join(
        [f"Context {i+1}: {segment}" for i, segment in enumerate(text_segments)]
    )
    prompt = ChatPromptTemplate.from_template(PROMPT)
    chain = prompt | model
    result = chain.invoke({"question": question, "contexts": formatted_segments})
    return result

def generate_embeddings(model: Embeddings):
    content = pymupdf.open("./files/aws-setup-guide.pdf")

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
                metadata={
                    "id": str(1),
                    "page_number": page.number
                }
            )
        )

    split_documents = text_splitter.split_documents(documents)
    vector_store = PGVector(
        embeddings=model,
        connection=TEST_DATABASE_URL,
        collection_name="docs_embeddings",
        use_jsonb=True
    )
    vector_store.add_documents(split_documents)


def test_model(df, embeddings_model: Embeddings, generative_model, model_name: str):

    vector_store = PGVector(
        embeddings=embeddings_model,
            connection=TEST_DATABASE_URL,
        collection_name="docs_embeddings",
        use_jsonb=True
    )
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    predictions = []
    for it, row in tqdm(df.iterrows(), total=1):
        print(f"Asking: {row['question']}")
        retrieved_docs = retriever.invoke(row["question"])
        content = []
        for doc in retrieved_docs:
            content.append(doc.page_content)
        response = get_response(row["question"], content, generative_model)
        print(f"Received response {response}")
        predictions.append(response)

    df[f"{model_name}_result"] = predictions


qa_df = pd.read_csv("./files/aws_setup_guide_dataset.csv")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyA30SVzB88AC4N_Y6TcllSLlVuFVwK8ptE")
generate_embeddings(embeddings)

gen_model= ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key="AIzaSyA30SVzB88AC4N_Y6TcllSLlVuFVwK8ptE"
)
test_model(qa_df, embeddings, gen_model, "wizardlm2:7b")
qa_df.to_csv("./files/models_test_responses.csv")