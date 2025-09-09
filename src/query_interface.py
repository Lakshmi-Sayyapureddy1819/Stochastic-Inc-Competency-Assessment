import google.generativeai as generativeai
from src.config import GOOGLE_API_KEY

generativeai.configure(api_key=GOOGLE_API_KEY)

def ask_document_qa_agent(document_text, user_query):
    prompt = f"""You are an AI assistant with access to the following document content:
{document_text}

Answer the question based on the document:
Q: {user_query}
A:"""

    try:
        response = generativeai.chat.completions.create(
            model="gemini-1.5-pro-latest",
            messages=[
                {"content": prompt, "role": "user"}
            ],
            temperature=0.2,
            max_output_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"
