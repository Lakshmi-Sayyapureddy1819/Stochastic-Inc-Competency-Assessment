import streamlit as st
import google.generativeai as genai
from src.config import GOOGLE_API_KEY
from src.ingestion import extract_text_from_pdf
from src.arxiv_integration import search_arxiv

# Configure Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

def ask_document_qa_agent(document_text, user_query):
    messages = [
        {
            "role": "system",
            "content": f"You are an AI assistant with access to this document content:\n{document_text}"
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(
            messages=messages,
            temperature=0.7,
            candidate_count=1
        )
        if response.candidates and len(response.candidates) > 0:
            # Use .content or .message depending on your version
            return response.candidates[0].content
        else:
            return "No candidates found in response."
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

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

def document_qa_chat():
    st.markdown('<div class="section-header">📄 Document Q&A Chatbot with Gemini API</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False

    if uploaded_file:
        with st.spinner("Extracting text..."):
            try:
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
                st.session_state.chat_history = []
                st.session_state.waiting_for_response = False
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
                st.session_state.document_text = None

    if st.session_state.document_text:
        with st.expander("📄 Document Text Preview"):
            st.text_area("Document Text", st.session_state.document_text, height=200, disabled=True)

        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["message"])

        if not st.session_state.waiting_for_response:
            prompt = st.chat_input("Ask a question about the document")
            if prompt:
                st.session_state.chat_history.append({"role": "user", "message": prompt})
                st.session_state.waiting_for_response = True

        if st.session_state.waiting_for_response:
            with st.spinner("Generating answer..."):
                answer = ask_document_qa_agent(st.session_state.document_text, st.session_state.chat_history[-1]["message"])
            st.session_state.chat_history.append({"role": "assistant", "message": answer})
            st.session_state.waiting_for_response = False

    else:
        st.info("Please upload a PDF document to begin.")

def arxiv_search_section():
    st.markdown('<div class="section-header">🔍 Search Research Papers on Arxiv</div>', unsafe_allow_html=True)
    arxiv_query = st.text_input("Enter keywords for Arxiv paper search:")
    if st.button("Search Papers"):
        if arxiv_query.strip():
            with st.spinner("Searching Arxiv..."):
                papers = search_arxiv(arxiv_query)
            if papers:
                for paper in papers:
                    st.markdown(f"**Title:** {paper['title']}")
                    st.markdown(f"**Summary:** {paper['summary']}")
                    st.markdown(f"[Read Paper]({paper['link']})")
                    st.markdown("---")
            else:
                st.info("No papers found for this query.")

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
