import requests
from src.config import GEMINI_API_KEY

def ask_document_qa_agent(document_text, user_query):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    url = "https://api.gemini.com/v1/completions"  # Replace with Gemini API real endpoint

    prompt = f"""You are an AI assistant with access to the following document content:
{document_text}

Answer the question based on the document:

Q: {user_query}
A:"""

    data = {
        "model": "gemini-1-large",  # Replace with actual Gemini model name
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.2,
        "n": 1,
        "stop": ["\n"]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["text"].strip()
