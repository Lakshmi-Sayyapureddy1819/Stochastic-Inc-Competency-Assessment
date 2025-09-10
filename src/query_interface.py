import google.generativeai as genai
from src.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def ask_document_qa_agent(document_text, user_query):
    prompt = f"""You are an AI assistant with access to the following document content:
{document_text}

Answer the question based on the document:
Q: {user_query}
A:"""

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text  # This is the generated answer

    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"
