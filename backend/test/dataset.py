import json
import re
import time

import pandas as pd
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# https://medium.com/@vndee.huynh/how-to-effectively-evaluate-your-rag-llm-applications-2139e2d2c7a4
QA_DATASET_GENERATION_PROMPT = PromptTemplate.from_template(
    "You are an expert on generate question-and-answer dataset based on a given context. You are given a context. "
    "Your task is to generate a question and answer based on the context. The generated question should be able to"
    " to answer by leverage the given context. And the generated question-and-answer pair must be grammatically "
    "and semantically correct. Your response must be in a json format with 2 keys: question, answer. For example,"
    "\n\n"
    "Context: France, in Western Europe, encompasses medieval cities, alpine villages and Mediterranean beaches. Paris, its capital, is famed for its fashion houses, classical art museums including the Louvre and monuments like the Eiffel Tower."
    "\n\n"
    "Response: {{"
    "\n"
    "    \"question\": \"Where is France and what is it’s capital?\","
    "\n"
    "    \"answer\": \"France is in Western Europe and it’s capital is Paris.\""
    "\n"
    "}}"
    "\n\n"
    "Context: The University of California, Berkeley is a public land-grant research university in Berkeley, California. Established in 1868 as the state's first land-grant university, it was the first campus of the University of California system and a founding member of the Association of American Universities."
    "\n\n"
    "Response: {{"
    "\n"
    "    \"question\": \"When was the University of California, Berkeley established?\","
    "\n"
    "    \"answer\": \"The University of California, Berkeley was established in 1868.\""
    "\n"
    "}}"
    "\n\n"
    "Now your task is to generate a question-and-answer dataset based on the following context:"
    "\n\n"
    "Ensure that the response is only the JSON output without additional text."
    "\n\n"
    "Context: {context}"
    "\n\n"
    "Response: ",
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key="AIzaSyA30SVzB88AC4N_Y6TcllSLlVuFVwK8ptE")
loader = PyMuPDFLoader(file_path="./files/aws-setup-guide.pdf")
chain = create_stuff_documents_chain(llm, QA_DATASET_GENERATION_PROMPT)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(loader.load())

questions, answers = [], []
i = 0
try:
    for chunk in chunks[63:]:
        response = chain.invoke({
            "context": [chunk]
        })
        clean_response = re.sub(r'^```(?:json)?\s*', '', response.strip())
        clean_response = re.sub(r'\s*```$', '', clean_response)

        try:
            print(clean_response)
            obj = json.loads(clean_response)
            questions.append(obj["question"])
            answers.append(obj["answer"])
        except json.JSONDecodeError as e:
            print(f"Error while decoding JSON: {e}")
            print(f"Received response:\n{response}")
        finally:
            if i%2 == 1:
                time.sleep(1)
            i += 1
except Exception as e:
    print(f"An exception has ocurred: {e}")

df = pd.DataFrame({
    "question": questions,
    "answer": answers
})

df.to_csv("./files/aws_setup_guide_dataset.csv", index=False)
