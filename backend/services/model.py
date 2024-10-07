import os
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI

def get_embedding_model() -> OllamaEmbeddings| GoogleGenerativeAIEmbeddings| OpenAIEmbeddings:
    model = os.environ['Model_Provider']
    if model == "ollama":
        return OllamaEmbeddings(model="wizardlm2:7b", base_url="ollama:11434")
    elif model == "gemini":
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    elif model == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-large")

def get_response_model() -> OllamaLLM | GoogleGenerativeAI | OpenAI:
    model = os.environ['Model_Provider']
    if model == "ollama":
        return OllamaLLM(model="wizardlm2:7b", base_url="ollama:11434", keep_alive=-1)
    elif model == "gemini":
        return GoogleGenerativeAI(model="gemini-pro")
    elif model == "openai":
        return OpenAI(model_name="gpt-3.5-turbo-instruct")