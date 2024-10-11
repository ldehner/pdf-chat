import json
from typing import Optional, Any

import numpy as np
import pandas as pd
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, wait_fixed, stop_after_attempt
from tqdm import tqdm

CORRECTNESS_PROMPT = PromptTemplate.from_template("""
Extract following from given question and ground truth. Your response must be in a json format with 3 keys and does not need to be in any specific order:
- statements that are present in both the answer and the ground truth
- statements present in the answer but not found in the ground truth
- relevant statements found in the ground truth but omitted in the answer
Please be concise and do not include any unnecessary information. You should classify the statements as claims, facts, or opinions with semantic matching, no need exact word-by-word matching.
Question:What powers the sun and what is its primary function?
Answer: The sun is powered by nuclear fission, similar to nuclear reactors on Earth, and its primary function is to provide light to the solar system.
Ground truth: The sun is actually powered by nuclear fusion, not fission. In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy. This energy is what lights up the sun and provides heat and light, essential for life on Earth. The sun's light also plays a critical role in Earth's climate system and helps to drive the weather and ocean currents.
Extracted statements:
[
{{
  "statements that are present in both the answer and the ground truth": ["The sun's primary function is to provide light"],
  "statements present in the answer but not found in the ground truth": ["The sun is powered by nuclear fission", "similar to nuclear reactors on Earth"],
  "relevant statements found in the ground truth but omitted in the answer": ["The sun is powered by nuclear fusion, not fission", "In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy", "This energy provides heat and light, essential for life on Earth", "The sun's light plays a critical role in Earth's climate system", "The sun helps to drive the weather and ocean currents"]
}}
]
Question: What is the boiling point of water?
Answer: The boiling point of water is 100 degrees Celsius at sea level.
Ground truth: The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit) at sea level, but it can change with altitude.
Extracted statements:
[
  {{
    "statements that are present in both the answer and the ground truth": ["The boiling point of water is 100 degrees Celsius at sea level"],
    "statements present in the answer but not found in the ground truth": [],
    "relevant statements found in the ground truth but omitted in the answer": ["The boiling point can change with altitude", "The boiling point of water is 212 degrees Fahrenheit at sea level"]
  }}
]

Do not include the question,answer and ground truth in the response. Only the extracted statements.
Question: {question}
Answer: {answer}
Ground truth: {ground_truth}
Extracted statements:""",
                                                  )


def parse_response(response: str) -> Optional[dict | list[dict]]:
    try:
        obj = json.loads(response)
        return obj[0]
    except json.decoder.JSONDecodeError:
        print(f"Exception parsing response:\n{response}\n")
        print(f"Retrying with response cleaning...")
        cleaned_response = response.strip("```json").strip("```")
        try:
            obj = json.loads(cleaned_response)
            return obj
        except json.decoder.JSONDecodeError:
            print(f"Exception parsing response:\n{cleaned_response}\n")
            return None


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def invoke_chain(chain, inputs):
    return chain.invoke(inputs)

def evaluate_correctness(model_name: str, df):
    judy_llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key="AIzaSyA30SVzB88AC4N_Y6TcllSLlVuFVwK8ptE",
        response_format={
            "type": "json_object"
        },
    )

    chain = LLMChain(llm=judy_llm, prompt=CORRECTNESS_PROMPT)

    key_map = {
        "TP": "statements that are present in both the answer and the ground truth",
        "FP": "statements present in the answer but not found in the ground truth",
        "FN": "relevant statements found in the ground truth but omitted in the answer",
    }

    TP, FP, FN = [], [], []

    errors = 0

    for it, row in tqdm(df.iterrows(), total=len(df)):
        print(f"Invoking with question: {row['question']}")
        resp = invoke_chain(chain, {
            "question": row["question"],
            "answer": row[model_name],
            "ground_truth": row["answer"]
        })
        obj = parse_response(resp["text"])
        if isinstance(obj, list):
            obj = obj[0]
        print(f"Response: {obj}")
        if obj is not None:
            TP.append(len(obj[key_map["TP"]]))
            FP.append(len(obj[key_map["FP"]]))
            FN.append(len(obj[key_map["FN"]]))
        else:
            errors += 1
            TP.append(-1)
            FP.append(-1)
            FN.append(-1)

    print(f"There were {errors} errors while judging responses\n")

    TP = np.array(TP)
    FP = np.array(FP)
    FN = np.array(FN)

    valid_indices = np.where(TP != -1)[0]

    TP_valid = TP[valid_indices]
    FP_valid = FP[valid_indices]
    FN_valid = FN[valid_indices]

    recall = np.where((TP_valid + FN_valid) != 0, TP_valid / (TP_valid + FN_valid), 0)
    precision = np.where((TP_valid + FP_valid) != 0, TP_valid / (TP_valid + FP_valid), 0)

    correctness = np.where((recall + precision) != 0, 2 * recall * precision / (recall + precision), 0)

    data = {"recall": recall, "precision": precision, "correctness": correctness}

    return pd.DataFrame(data)


responses_df = pd.read_csv("./files/sanitized_models_test_responses.csv")
result_df = evaluate_correctness("gemini", responses_df)
result_df.to_csv("./files/result_values.csv")

recall_mean = result_df["recall"].astype(float).mean()
precision_mean = result_df["precision"].astype(float).mean()
correctness_mean = result_df["correctness"].astype(float).mean()
print(
    f"|gemini-1.5-pro     |    {recall_mean:.4f}    |     {precision_mean:.4f}    |     {correctness_mean:.4f}      |")
