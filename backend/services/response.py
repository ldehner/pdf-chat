from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI
from services.model import get_response_model

def get_response(question: str, text_segments: List[str]) -> str:
    template = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {contexts} 
    Answer:
    """

    formatted_segments = "\n".join(
        [f"Context {i+1}: {segment}" for i, segment in enumerate(text_segments)]
    )
    prompt = ChatPromptTemplate.from_template(template)
    model = get_response_model()
    chain = prompt | model
    result = chain.invoke({"question": question, "contexts": formatted_segments})
    return result


def preload_model():
    model = get_response_model()
    chain = model
    chain.invoke("")
