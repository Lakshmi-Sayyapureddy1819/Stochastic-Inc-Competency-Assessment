import streamlit as st
from src.ingestion import extract_text_from_pdf
from src.query_interface import ask_document_qa_agent
from src.arxiv_integration import search_arxiv

def main():
    st.set_page_config(page_title="Document Q&A AI Agent", page_icon="🤖", layout="wide")
    st.title("Document Q&A AI Agent with Gemini API")

    # Initialize session state variables
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    if uploaded_file:
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Extracting text from PDF..."):
            st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
        st.success("PDF text extracted successfully!")
        st.session_state.qa_history = []  # Clear previous Q&A on new upload

    # Show extracted text (optional)
    if st.session_state.document_text:
        with st.expander("Show extracted document text (optional)"):
            st.text_area("Document Text", st.session_state.document_text, height=300, disabled=True)

        # Multiple question input
        user_query = st.text_input("Ask a question about the document:")

        if st.button("Get Answer") and user_query.strip():
            with st.spinner("Generating answer..."):
                answer = ask_document_qa_agent(st.session_state.document_text, user_query)
            st.session_state.qa_history.append({"question": user_query, "answer": answer})

        # Display Q&A history
        if st.session_state.qa_history:
            st.markdown("### Question and Answer History:")
            for i, qa in enumerate(st.session_state.qa_history):
                st.markdown(f"**Q{i+1}:** {qa['question']}")
                st.markdown(f"**A{i+1}:** {qa['answer']}")
                st.markdown("---")

    st.markdown("---")

    # Arxiv Paper Search Section
    st.header("Search Research Papers on Arxiv")
    arxiv_query = st.text_input("Enter keywords for Arxiv paper search:", key="arxiv_query")
    if st.button("Search Arxiv Papers"):
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

if __name__ == "__main__":
    main()
