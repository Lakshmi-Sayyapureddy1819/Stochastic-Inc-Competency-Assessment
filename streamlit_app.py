import streamlit as st
import google.generativeai as genai
from src.config import GOOGLE_API_KEY
from src.ingestion import extract_text_from_pdf
from src.arxiv_integration import search_arxiv

# -------------------------------
# Gemini API setup
# -------------------------------
genai.configure(api_key=GOOGLE_API_KEY)

def ask_document_qa_agent(document_text, user_query):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(
            f"You are an AI assistant with access to this document:\n\n{document_text}\n\n"
            f"User question: {user_query}"
        )
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text
        return "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ Error calling Gemini API: {str(e)}"


# -------------------------------
# Custom CSS
# -------------------------------
def inject_css():
    image_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1470&q=80"
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            padding-top: 1rem;
        }}
        .sidebar .sidebar-content {{
            background: rgba(211, 204, 227, 0.85);
            padding: 1rem;
        }}
        .stChatMessage {{
            font-size: 1.1rem;
        }}
        .section-header {{
            border-bottom: 2px solid #ddd;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }}
    </style>
    """, unsafe_allow_html=True)


# -------------------------------
# Document Q&A Chat
# -------------------------------
def document_qa_chat():
    st.markdown('<div class="section-header">📄 Document Q&A Chatbot with Gemini API</div>', unsafe_allow_html=True)

    # Upload always visible
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    if uploaded_file and "document_text" not in st.session_state:
        with st.spinner("Extracting text..."):
            st.session_state.document_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Document uploaded and processed.")

    # If no doc → stop here
    if "document_text" not in st.session_state:
        st.info("Please upload a PDF to begin chatting.")
        return

    # Chat history setup
    if "doc_chat_history" not in st.session_state:
        st.session_state.doc_chat_history = []

    # Show previous messages
    for chat in st.session_state.doc_chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # Handle new user input
    if prompt := st.chat_input("Ask a question about your document..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.doc_chat_history.append({"role": "user", "message": prompt})

        with st.spinner("Generating answer..."):
            answer = ask_document_qa_agent(st.session_state.document_text, prompt)

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.doc_chat_history.append({"role": "assistant", "message": answer})


# -------------------------------
# Arxiv Search
# -------------------------------
def arxiv_search_section():
    st.markdown('<div class="section-header">🔍 Search Research Papers on Arxiv</div>', unsafe_allow_html=True)
    query = st.text_input("Enter keywords for Arxiv paper search:")
    if st.button("Search Papers"):
        if query.strip():
            with st.spinner("Searching Arxiv..."):
                papers = search_arxiv(query)
            if papers:
                for paper in papers:
                    st.markdown(f"**Title:** {paper['title']}")
                    st.markdown(f"**Summary:** {paper['summary']}")
                    st.markdown(f"[Read Paper]({paper['link']})")
                    st.markdown("---")
            else:
                st.info("No papers found for this query.")


# -------------------------------
# Main
# -------------------------------
def main():
    inject_css()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose Section", ["Document Q&A Chatbot", "Arxiv Paper Search"])
    if page == "Document Q&A Chatbot":
        document_qa_chat()
    else:
        arxiv_search_section()


if __name__ == "__main__":
    main()
