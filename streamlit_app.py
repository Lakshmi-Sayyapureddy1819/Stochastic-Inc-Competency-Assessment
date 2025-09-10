import streamlit as st
import google.generativeai as genai
from src.config import GOOGLE_API_KEY
from src.ingestion import extract_text_from_pdf
from src.arxiv_integration import search_arxiv

# Configure Google API
genai.configure(api_key=GOOGLE_API_KEY)

# =========================
# Helper Functions
# =========================
def ask_document_qa_agent(document_text, question):
    """
    Send the document text and user question to Gemini API for Q&A.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ correct model
    response = model.generate_content(f"Context:\n{document_text}\n\nQuestion: {question}")
    return response.text


def ask_arxiv_agent(query):
    """
    Search Arxiv and return formatted results.
    """
    results = search_arxiv(query)
    if not results:
        return "No results found."
    formatted = "\n\n".join([f"📌 **{r['title']}**\n{r['summary']}\n🔗 {r['link']}" for r in results])
    return formatted


# =========================
# Document Q&A Chat
# =========================
def document_qa_chat():
    st.subheader("📄 Document Q&A Chatbot")

    if "doc_chat_history" not in st.session_state:
        st.session_state.doc_chat_history = []

    if "document_text" not in st.session_state:
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if uploaded_file:
            st.session_state.document_text = extract_text_from_pdf(uploaded_file)
            st.success("✅ Document uploaded and processed.")
        else:
            st.info("Please upload a PDF to start chatting.")
            return

    # Show chat history
    for chat in st.session_state.doc_chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # Input
    if prompt := st.chat_input("Ask a question about your document..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.doc_chat_history.append({"role": "user", "message": prompt})

        try:
            response = ask_document_qa_agent(st.session_state.document_text, prompt)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.doc_chat_history.append({"role": "assistant", "message": response})


# =========================
# Arxiv Paper Search Chat
# =========================
def arxiv_chat():
    st.subheader("🔎 Arxiv Paper Search")

    if "arxiv_chat_history" not in st.session_state:
        st.session_state.arxiv_chat_history = []

    # Show chat history
    for chat in st.session_state.arxiv_chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # Input
    if query := st.chat_input("Search Arxiv papers..."):
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.arxiv_chat_history.append({"role": "user", "message": query})

        try:
            response = ask_arxiv_agent(query)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.arxiv_chat_history.append({"role": "assistant", "message": response})


# =========================
# Main App
# =========================
def main():
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Choose Section", ["Document Q&A Chatbot", "Arxiv Paper Search"])

    if section == "Document Q&A Chatbot":
        document_qa_chat()
    elif section == "Arxiv Paper Search":
        arxiv_chat()


if __name__ == "__main__":
    main()
