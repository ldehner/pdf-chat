import pandas as pd

def sanitize(text):
    text = text[len("content='"):]
    text = text.split(r'\n', 1)[0]
    return text

df = pd.read_csv("./files/models_test_responses.csv")
gemini_columns = [col for col in df.columns if "gemini" in col]
for col in gemini_columns:
    df[col] = df[col].apply(sanitize)

df.to_csv('./files/sanitized_models_test_responses.csv', index=False)