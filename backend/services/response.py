from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


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
    model = OllamaLLM(model="llama3.2:1b", base_url="ollama:11434")
    chain = prompt | model
    result = chain.invoke({"question": question, "contexts": formatted_segments})
    return result
