from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def get_response(question: str, text_segments: List[str]) -> str:
    template = """Question: {question}

    {contexts}
    
    Answer: If context is given, answer only based on the context - thats very important. If context is not given, answer based on general knowledge. Answer in 1 to 5 sentences."""

    formatted_segments = "\n".join(
        [f"Context {i+1}: {segment}" for i, segment in enumerate(text_segments)]
    )
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="wizardlm2:7b", base_url="ollama:11434", keep_alive=-1)
    chain = prompt | model
    result = chain.invoke({"question": question, "contexts": formatted_segments})
    return result


def preload_model():
    model = OllamaLLM(model="wizardlm2:7b", base_url="ollama:11434", keep_alive=-1)
    chain = model
    chain.invoke("")
