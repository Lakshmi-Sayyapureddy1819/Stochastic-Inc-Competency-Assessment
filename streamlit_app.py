import streamlit as st
import google.generativeai as genai
from src.config import GOOGLE_API_KEY
from src.ingestion import extract_text_from_pdf
from src.arxiv_integration import search_arxiv

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)


# ============ DOCUMENT QA CHATBOT ============
def ask_document_qa_agent(document_text, question):
    """Call Gemini API to answer question based on document text."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"Based on this document, answer the following question:\n\nDocument: {document_text}\n\nQuestion: {question}"
        )
        return response.text if response and hasattr(response, "text") else "⚠️ No response from Gemini API."
    except Exception as e:
        return f"⚠️ Error: {e}"


def document_qa_chat():
    st.markdown('<div class="section-header">📄 Document Q&A Chatbot</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    # Session state
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Process PDF
    if uploaded_file:
        with st.spinner("Extracting text..."):
            try:
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
                st.session_state.chat_history = []
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
                st.session_state.document_text = None

    # Chatbot UI
    if st.session_state.document_text:
        with st.expander("📄 Document Preview"):
            st.text_area("Document Text", st.session_state.document_text, height=200, disabled=True)

        # Show chat history
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["message"])

        # Chat input
        prompt = st.chat_input("Ask a question about the document")
        if prompt:
            # Display user message
            st.session_state.chat_history.append({"role": "user", "message": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate assistant response instantly
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_document_qa_agent(st.session_state.document_text, prompt)
                    st.markdown(answer)

            # Save assistant reply
            st.session_state.chat_history.append({"role": "assistant", "message": answer})
    else:
        st.info("Please upload a PDF document to begin.")


# ============ ARXIV PAPER SEARCH ============
def arxiv_paper_search():
    st.markdown('<div class="section-header">📚 Arxiv Paper Search</div>', unsafe_allow_html=True)
    query = st.text_input("Enter a research topic to search papers:")
    if query:
        with st.spinner("Searching Arxiv..."):
            try:
                results = search_arxiv(query)
                if results:
                    for paper in results:
                        st.markdown(f"### [{paper['title']}]({paper['url']})")
                        st.markdown(f"**Authors:** {paper['authors']}")
                        st.markdown(f"**Published:** {paper['published']}")
                        st.markdown(f"**Summary:** {paper['summary'][:500]}...")
                        st.markdown("---")
                else:
                    st.warning("No results found.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")


# ============ MAIN APP ============
def main():
    st.set_page_config(page_title="Knowledge Assistant", layout="wide")
    st.title("🔍 Knowledge Assistant")

    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Choose Section", ["Document Q&A Chatbot", "Arxiv Paper Search"])

    if section == "Document Q&A Chatbot":
        document_qa_chat()
    elif section == "Arxiv Paper Search":
        arxiv_paper_search()


if __name__ == "__main__":
    main()
