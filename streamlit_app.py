import streamlit as st
from src.ingestion import extract_text_from_pdf
from src.query_interface import ask_document_qa_agent
from src.arxiv_integration import search_arxiv

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
    </style>
    """, unsafe_allow_html=True)

def document_qa_interface():
    st.title("📄 Document Q&A Chatbot with Gemini API")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "new_message" not in st.session_state:
        st.session_state.new_message = False

    if uploaded_file:
        with st.spinner("Extracting text..."):
            with open("temp_uploaded.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
            st.session_state.chat_history = []
        st.success("PDF loaded! Start asking questions.")

    if st.session_state.document_text:
        with st.expander("📄 Document Text Preview"):
            st.text_area("Document Text", st.session_state.document_text, height=200, disabled=True)

        # Display all chat messages
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["message"])

        prompt = st.chat_input("Ask a question about the document")

        if prompt or st.session_state.new_message:
            if prompt:
                st.session_state.chat_history.append({"role": "user", "message": prompt})
                with st.spinner("Generating answer..."):
                    answer = ask_document_qa_agent(st.session_state.document_text, prompt)
                st.session_state.chat_history.append({"role": "assistant", "message": answer})
                st.session_state.new_message = True

            st.session_state.new_message = False

    else:
        st.info("Please upload a PDF document to begin.")

def arxiv_search_interface():
    st.title("🔍 Search Research Papers on Arxiv")
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
    page = st.sidebar.radio("Go to", ["Document Q&A Chatbot", "Arxiv Paper Search"])
    if page == "Document Q&A Chatbot":
        document_qa_interface()
    elif page == "Arxiv Paper Search":
        arxiv_search_interface()

if __name__ == "__main__":
    main()
